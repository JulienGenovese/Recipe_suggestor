from abc import ABC, abstractmethod

class Ricetta(ABC):
    def __init__(self):
        """
        Costruttore che legge tutti i file Excel da una folder specifica
        e carica i dati in dizionari.
        
        :param folder: La folder contenente i file Excel da leggere.
        """
        self.nome = None
        self.ingredienti = None
        self.procedimento = None
    
    def processa_ricetta(*args):
        raise NotImplementedError
    
class RicettaFromPdfWithOpenAI(Ricetta):
    def processa_ricetta(pagina_pdf):
        ricetta_prompt_str = generate_richiesta_ricetta(raw_text[i])

    
    @staticmethod
    def generate_richiesta_ricetta(ricetta_str):
        prompt = f"""Il testo seguente è una ricetta in inglese.
        Estrai in italiano il Nome, gli ingredienti, e il Procedimento nel seguento formato:
        Nome: <inserisci nome>
        Ingredienti: <inserisci ingredienti>
        Procedimento: <inserisci procedimento>
        ###
        '{ricetta_str}'
        ###
        """
        return prompt
    
    
    
