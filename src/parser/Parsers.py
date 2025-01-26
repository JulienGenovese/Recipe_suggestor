from abc import ABC, abstractmethod
from PyPDF2 import PdfReader
from openai import OpenAI
import sys 
sys.path.append("src")
from Config import Config
import os
import re
import json


def clean_string(ingredient):
    # Rimuove simboli iniziali come #, -, *, e qualsiasi spazio extra
    ingredient = ingredient.strip()
    return re.sub(r'^[#*-]+\s*', '', ingredient)

class AbstractParser(ABC):
    def __init__(self, folder_dati: str, file_name: str):
        self.ricettario_path = os.path.join(folder_dati, file_name)
        self.folder_dati = folder_dati
        self.file_name = file_name 
        self.dict_ricette_parsate = None
        assert os.path.exists(self.ricettario_path), f"{self.ricettario_path} doesn't exists"

    @abstractmethod
    def estrai_dict_ricetta_from_page(self):
        raise NotImplementedError

    @abstractmethod
    def read_ricettario(self):
        raise NotImplementedError

    def return_ricette(self) -> None:
        if self.dict_ricette_parsate is not None:
            return self.dict_ricette_parsate
        else:
            raise ValueError("The text must be extracted first. No recette are found")
        
    def write_to_json(self, path_folder_destination):
        file_name = self.file_name.replace("pdf", "json")
        path_file = os.path.join(path_folder_destination, file_name)
        ricette_dict = self.return_ricette()
        # Write the dictionary to a JSON file
        with open(path_file, 'w', encoding='utf-8') as f:
            json.dump(ricette_dict, f, ensure_ascii=False, indent=4)

class PdfParser(AbstractParser):
    def __init__(self, folder_dati: str, 
                 file_name: str,
                 starting_page_recipe: int = None, 
                 ending_page_recipe: int = None):
        self.starting_page_recipe = starting_page_recipe
        self.ending_page_recipe = ending_page_recipe    
        super().__init__(folder_dati=folder_dati,
                         file_name=file_name
        )
        self.pdf_reader = PdfReader(self.ricettario_path)

    @abstractmethod
    def estrai_dict_ricetta_from_page(self):
        raise NotImplementedError

    def read_ricettario(self):
        self.read_raw_text_from_pdf()
        self.estrai_ricettario_from_pdf()

    def read_raw_text_from_pdf(self):
        dict_ricettario_raw = {}
        pages_to_read = self.pdf_reader.pages[self.starting_page_recipe:self.ending_page_recipe]
        for i, page in enumerate(pages_to_read):
            content = page.extract_text()
            if content:
                dict_ricettario_raw[i+self.starting_page_recipe] = content
        assert dict_ricettario_raw != {}, "No recipes found"
        self.dict_ricettario_raw = dict_ricettario_raw

    def estrai_ricettario_from_pdf(self) -> None:
        assert self.dict_ricettario_raw is not None, "You must first read the pdf with the '.read_ricettario()' method"
        dict_ricette_parsate = {}
        for pagina, testo in self.dict_ricettario_raw.items():
            dict_ricetta = self.estrai_dict_ricetta_from_page(pagina ,testo)
            dict_ricette_parsate[pagina] = dict_ricetta
        self.dict_ricette_parsate = dict_ricette_parsate

class ParserFromPdfWithOpenAI(PdfParser):
    def __init__(self, 
                 folder_dati: str,
                 file_name: str, 
                 config_obj: Config,
                 starting_page_recipe: int = None, 
                 ending_page_recipe: int = None,
                 model: str = "gpt-4o-mini"):
        api_key = config_obj.get("api", "key")
        self.client_openai = OpenAI(api_key=api_key)
        self.allow_cost = False
        self.model = model
        self.temperature = 0.2

        super().__init__(folder_dati=folder_dati, 
                         file_name=file_name,
                         starting_page_recipe=starting_page_recipe, 
                         ending_page_recipe=ending_page_recipe)

    @staticmethod
    @abstractmethod
    def convert_ricetta_str_to_dict(text: str) -> dict:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def generate_prompt_ricetta(ricetta_str: str) -> str:
        raise NotImplementedError
    
    def allow_compute_cost(self):
        self.allow_cost = True
    
    def calculate_cost(self, prompt_tokens, completion_tokens):
        pricing_mil_tok= {
            "gpt-4o": {"prompt": 2.50, "completion": 10},
            "gpt-4o-mini": {"prompt": 0.150, "completion": 0.06},
            "o1": {"prompt": 15, "completion": 60},
            "o1-mini": {"prompt": 3, "completion": 12},
        }

        if self.model not in pricing_mil_tok:
            raise ValueError(f"Pricing for model {self.model} not found.")

        prompt_cost = (prompt_tokens / 1E6) * pricing_mil_tok[self.model]["prompt"]
        completion_cost = (completion_tokens / 1E6) * pricing_mil_tok[self.model]["completion"]
        return prompt_cost + completion_cost
    
    def call_openai(self, prompt: str) -> str:
        print("Calling OpenAI. Generating output...")
        if "gpt" in self.model:
            stream = self.client_openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                temperature=self.temperature
            )
        elif "o1" in self.model:
            stream = self.client_openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
        else:
            raise ValueError("Strange model")
        
        ricetta = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                ricetta += content
        if self.allow_cost:
            response = self.client_openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            usage = response.usage
            prompt_tokens = usage.prompt_tokens
            completion_tokens = usage.completion_tokens
            cost = self.calculate_cost(prompt_tokens, completion_tokens)
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Completion tokens: {completion_tokens}")
            print(f"Total cost: ${cost:.6f}")
        print("...Output generated.")
        return ricetta

    def estrai_dict_ricetta_from_page(self, pagina: int, testo: str) -> dict:
        ricetta_prompt_str = self.generate_prompt_ricetta(testo)
        print("Reading page: ", pagina)
        if ricetta_prompt_str != "":
            ricetta_str = self.call_openai(prompt=ricetta_prompt_str)
            dict_ricetta = self.convert_ricetta_str_to_dict(ricetta_str)
        else:
            dict_ricetta = None
        return dict_ricetta
    
    @abstractmethod
    def generate_prompt_ricetta(ricetta_str: str, lingua_originale: str, lingua_target: str):
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def convert_ricetta_str_to_dict(text: str) -> dict:
        raise NotImplementedError

   
class ParserEasyRecipsForOneOrTwo(ParserFromPdfWithOpenAI):
    
    def __init__(self, 
                 folder_dati: str,
                 file_name: str, 
                 config_obj: Config,
                 starting_page_recipe: int = None, 
                 ending_page_recipe: int = None,
                 lingua_originale: str = "Inglese",
                 lingua_target: str = "Italiano",
                 model: str = "gpt-4o-mini"):
        self.lingua_originale = lingua_originale
        self.lingua_target = lingua_target
        super().__init__(folder_dati=folder_dati, 
                         file_name=file_name,
                         config_obj=config_obj,
                         starting_page_recipe=starting_page_recipe, 
                         ending_page_recipe=ending_page_recipe,
                         model=model)
        

    def generate_prompt_ricetta(self, ricetta_str: str) -> str:
        prompt = f"""
            Hai una pagina in {self.lingua_originale}. 
            Hai due task:
            1. Valuta se e' una ricetta, ovvero ha un nome, degli ingredienti, un procedimento, restituisci solo una stringa vuota senza nient'altro.
            2. Se e' una ricetta la tua seconda attività è di tradurla e organizzarla in {self.lingua_target} nel seguente formato:
                Nome: <nome della ricetta in {self.lingua_target}> 
                Ingredienti:
                    .<elenco degli ingredienti in {self.lingua_target} seguiti dalla quantità mediante un "-". Fai molta attenzione e metti eventuali frazioni come "1/2" o "3/4" invece di simboli come "½", "¾", messi sempre all'inizio della riga>
                Procedimento: 
                    <descrivi il procedimento in {self.lingua_target} passo per passo>

                Tipo: <predici se è un una colazione, un primo piatto, un contorno, un secondo, un piatto unico o un dolce>
                Difficoltà: <predici che difficoltà ha con un numero tra 1 (ricetta veloce e accessibile a tutti) e 5 (ricetta elaborata per cui è richiesta conoscenza dettagliata della cucina)
                Esegui i task nel seguente modo: 
                    1. Valuta prima se e' una ricetta
                     Non aggiungere spiegazioni o altri dettagli.
                    2. Assicurati di sostituire i simboli frazionari con il loro equivalente in formato 'numeratore/denominatore'.
                    
                Ecco la pagina in {self.lingua_target} da tradurre e organizzare:
                ---
                '{ricetta_str}'
                ---
        """
        return prompt
    
    @staticmethod
    def convert_ricetta_str_to_dict(text: str) -> dict:
        # Suddividi il testo nelle diverse sezioni
        try:
            sections = re.split(r"\n(?=[A-Za-z])", text.strip())
            
            # Estrai il nome della ricetta
            recipe_name = sections[0].split(":")[1].strip()
            
            # Estrai gli ingredienti
            ingredients_text = sections[1].split(":")[1].strip()
            ingredients = [ingredient.replace(".", "").strip() for ingredient in ingredients_text.split("\n")]
            
            # Estrai il procedimento
            procedure_text = sections[2].split(":")[1].strip()
            procedure_steps = [step.strip() for step in procedure_text.split("\n") if step]
            
            tipo_text = sections[3].split(":")[1].strip()
            difficolta_text = sections[4].split(":")[1].strip()

            # Crea il dizionario
            recipe_dict = {
                "nome": recipe_name,
                "tipo": tipo_text,
                "ingredienti": ingredients,
                "procedimento": procedure_steps,
                "difficolta": difficolta_text
            }
        except: 
            print("Error in splliting in sections. Recipe:\n")
            print(text)
            raise RuntimeError
        
        return recipe_dict

if __name__ == "__main__":
    path_ricette = os.path.join("data", "ricette_to_elaborate")
    path_ricette_elaborate = os.path.join("data", "ricette")

    file_name = "easy-recipes-for-one-or-two.pdf"

    config = Config()
    parser = ParserEasyRecipsForOneOrTwo(  
          model= "gpt-4o-mini",
          folder_dati=path_ricette,
          file_name=file_name, 
          config_obj=config,
          starting_page_recipe=41, 
          ending_page_recipe=42
      )
    parser.allow_compute_cost()
    parser.read_ricettario()
    ricette = parser.return_ricette()
    print(ricette)
    parser.write_to_json(path_ricette_elaborate)

    
    
    
    
    