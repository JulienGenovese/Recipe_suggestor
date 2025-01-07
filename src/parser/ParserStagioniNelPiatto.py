import json
import pdfplumber
import re
import os


class ParserStagioniNelPiatto:
    def __init__(self, folder_dati, file_name):
        self.pdf_path = os.path.join(folder_dati, file_name)
        self.folder_dati = folder_dati
        self.file_name = file_name 
        assert os.path.exists(self.pdf_path), f"{self.pdf_path} doesn't exists"
        self.ricette = None
        # Regex per identificare i tipi di piatti
        self.tipo_regex = {
            "dolce": r"\bdolci?\b",  # Cerca "dolce" o "dolci"
            "antipasto": r"\b(antipasto|antipasti)\b",  # Cerca "antipasto" o "antipasti"
            "primo": r"\b(primo piatto|primi piatti|primo|primi)\b",  # Cerca "primo piatto" o "primi piatti"
            "secondo": r"\b(secondo piatto|secondi piatti|secondo|secondi)\b",  # Cerca "secondo piatto", "secondi piatti", "secondo"
            "contorno": r"\b(contorno|contorni)\b",  # Cerca "secondo piatto", "secondi piatti", "secondo"
            "piatto_unico": r"\b(piatti|piatto)\b"
        }
        self.altezza_nome_ricetta = 100

    def estrai_dict_ricetta_from_pdf(self):
        """Estrae il testo da un PDF dove il contenuto è diviso in due colonne (sinistra e destra) in base alla parola 'Procedimenti'."""
        testo_completo = {}

        with pdfplumber.open(self.pdf_path) as pdf:
            for i, pagina in enumerate(pdf.pages):  # Limita a 15 pagine
                words = pagina.extract_words()

                # Trova la posizione della parola "Procedimenti"
                procedimenti_pos_y = None
                procedimenti_pos_x = None
                for word in words:
                    if "procedimento" in word['text'].lower():
                        procedimenti_pos_x = word['x0']  # Salviamo la posizione della parola "Procedimenti"
                        procedimenti_pos_y = word['bottom']
                        break
                
                if procedimenti_pos_x is not None and procedimenti_pos_y is not None:
                    # Dividiamo il testo in ingredienti e procedimento
                    ingredienti = []
                    procedimento = []
                    nome = ""
                    tipo = "altro"  # Default tipo

                    for word in words:
                        # Se la parola è a sinistra di "Procedimenti", è un ingrediente
                        if word['x0'] < procedimenti_pos_x and word['bottom'] > procedimenti_pos_y:
                            ingredienti.append(word)
                        # Se la parola è a destra di "Procedimenti", è il procedimento
                        elif word['x0'] >= procedimenti_pos_x and word['bottom'] > procedimenti_pos_y:
                            procedimento.append(word)
                        elif word['bottom'] < procedimenti_pos_y:
                            if tipo == "altro" and  word["bottom"] > self.altezza_nome_ricetta:
                                tipo = self.processa_parola(word)  # Assegna tipo
                            if word["bottom"] < self.altezza_nome_ricetta:
                                nome += " " + word["text"]
                        
                    # Processamento degli ingredienti
                    ingredienti_list = self.processa_ingredienti(ingredienti)

                    # Processamento del procedimento
                    procedimenti_list = self.processa_procedimento(procedimento)

                    # Combina i dati
                    testo_completo[i] = {
                        "nome": nome.lower().strip(),
                        "tipo": tipo,
                        "ingredienti": ingredienti_list,
                        "procedimento": "\n".join(procedimenti_list)
                    }
    
        self.ricette = testo_completo

    def return_ricette(self):
        if self.ricette is not None:
            return self.ricette
        else:
            raise ValueError("The text must be extracted from pdf. No recette are found")
        
    def processa_parola(self, word):
        """Elabora la parola per determinare il tipo di ricetta."""
        for tipo_key, regex in self.tipo_regex.items():
            if re.search(regex, word['text'], re.IGNORECASE):
                return tipo_key
        return "altro"

    def processa_ingredienti(self, ingredienti):
        """Processa la lista degli ingredienti."""
        rows_ingredienti = ""
        ingredienti_list = []
        previous_word = None
        for word in ingredienti:
            if previous_word is not None:
                if word["bottom"] == previous_word["bottom"]:  # Stessa riga
                    rows_ingredienti += " " + word["text"]
                else:
                    if rows_ingredienti.strip() and "per" not in rows_ingredienti.lower():
                        ingredienti_list.append(rows_ingredienti.strip())
                    rows_ingredienti = word["text"]  # Nuova riga
            else:
                rows_ingredienti += word["text"]
            previous_word = word

        # Aggiungi l'ultimo ingrediente (se c'è)
        if rows_ingredienti.strip():
            ingredienti_list.append(rows_ingredienti.strip())

        return ingredienti_list

    def processa_procedimento(self, procedimento):
        """Processa la lista del procedimento."""
        rows_procedimenti = ""
        procedimenti_list = []
        previous_word = None
        for word in procedimento:
            if previous_word is not None:
                if word["bottom"] == previous_word["bottom"]:  # Stessa riga
                    rows_procedimenti += " " + word["text"]
                else:
                    procedimenti_list.append(rows_procedimenti.strip())
                    rows_procedimenti = word["text"]  # Nuova riga
            else:
                rows_procedimenti += word["text"]
            previous_word = word

        # Aggiungi l'ultimo passo del procedimento (se c'è)
        if rows_procedimenti.strip():
            procedimenti_list.append(rows_procedimenti.strip())

        return procedimenti_list
    
    def write_to_json(self, path_folder):
        file_name = self.file_name.replace("pdf", "json")
        path_file = os.path.join(path_folder, file_name)
        ricette_dict = self.return_ricette()
        # Write the dictionary to a JSON file
        with open(path_file, 'w', encoding='utf-8') as f:
            json.dump(ricette_dict, f, ensure_ascii=False, indent=4)
        
    

if __name__ == "__main__":
    import os 
    folder_dati = r"data\ricette_to_elaborate"
    file_name = "Le-ricette-di-stagioni-nel-piatto-ricettario-ebook.pdf"
    parser = ParserStagioniNelPiatto(folder_dati, file_name)
    parser.estrai_dict_ricetta_from_pdf()
    result = parser.return_ricette()
    #print(result)