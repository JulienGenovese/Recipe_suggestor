import json
import os

class Ricettario:
    def __init__(self, folder=r"data/ricette"):
        """
        Costruttore che legge tutti i file Excel da una folder specifica
        e carica i dati in dizionari.
        
        :param folder: La folder contenente i file Excel da leggere.
        """
        self.folder = folder
        self.dict_ricettario_completo = {}
        self.ricettario = {}
        self.carica_ricette()
        self.smista_ricette()

    def __str__(self):
       """
       Rappresentazione in stringa della classe Ricettario per stamparne il contenuto.
       """
       return f"Ricettario:\n\n" \
              f"Antipasti: {len(self.ricettario['antipasti'])}\n" \
              f"Primi: {len(self.ricettario['primi'])}\n" \
              f"Secondi: {len(self.ricettario['secondi'])}\n" \
              f"Contorni: {len(self.ricettario['contorni'])}\n" \
              f"Dolci: {len(self.ricettario['dolci'])}\n" \
              f"Piatti unici: {len(self.ricettario['piatti_unici'])}\n"
    def smista_ricette(self):
        """
        Smista le ricette nel dizionario in base al tipo e le memorizza nei rispettivi attributi.
        
        :param ricette: Un dizionario contenente le ricette.
        """
        
        self.ricettario["primi"] = []
        self.ricettario["secondi"] = []
        self.ricettario["antipasti"] = []
        self.ricettario["dolci"] = []
        self.ricettario["piatti_unici"] = []
        self.ricettario["contorni"] = []

        for ricetta in self.dict_ricettario_completo.values():
            tipo = ricetta.get("tipo").lower()  # Prendi il tipo della ricetta, in minuscolo per evitare errori di capitalizzazione

            # Smista la ricetta in base al tipo
            if tipo == "primo":
                self.ricettario["primi"].append(ricetta)
            elif tipo == "secondo":
                self.ricettario["secondi"].append(ricetta)
            elif tipo == "antipasto":
                self.ricettario["antipasti"].append(ricetta)
            elif tipo == "dolce":
                self.ricettario["dolci"].append(ricetta)
            elif tipo == "piatto_unico":
                self.ricettario["piatti_unici"].append(ricetta)
            elif tipo == "contorno":
                self.ricettario["contorni"].append(ricetta)
            else:
                # Se il tipo non è riconosciuto, puoi decidere se metterlo in una lista "altro" o ignorarlo
                raise ValueError(f"Tipo non riconosciuto: {tipo} per {ricetta.get('nome')}")

    def carica_ricette(self):
        """
        Carica i dati da tutti i file Excel nella folder specificata.
        Ogni file Excel viene trattato come un insieme di ricette, con ogni foglio come una lista di dizionari.
        """
        # Scansiona la folder per trovare i file json (.json)
        for filename in os.listdir(self.folder):
            if filename.endswith(".json"):
                percorso_file = os.path.join(self.folder, filename)
                self.leggi_json(percorso_file)

    def leggi_json(self, percorso_file):
        """
        Legge un file JSON e converte i dati in un dizionario.
        
        :param percorso_file: Il percorso completo del file JSON.
        """
        # Apri e leggi il file JSON
        with open(percorso_file, 'r', encoding='utf-8') as f:
            # Carica i dati dal file JSON
            dati_json = json.load(f)
        
        # Converte i dati in un dizionario
        for chiave, ricetta in dati_json.items():
            # Memorizza ogni ricetta nel dizionario self.dict_ricettario_completo
            self.dict_ricettario_completo[chiave] = ricetta

        print(f"Le ricette sono state lette correttamente dal file JSON: {percorso_file}")


    def mostra_ricette(self):
        """
        Mostra tutte le ricette caricate dalla folder Excel.
        """
        for chiave, ricetta in self.dict_ricettario_completo.items():
            print(f"File: {chiave}")
            print(ricetta)

if __name__ == "__main__":
    # Esempio di utilizzo:
    folder = r"data/ricette"  # Sostituisci con il percorso della tua folder
    ricette = Ricettario(folder)
    print(ricette)