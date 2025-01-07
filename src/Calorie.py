import pandas as pd
from utils import pulisci_stringa
class Calorie:
    def __init__(self, percorso_excel="data/calorie/calorie.xlsx"):
        """
        Costruttore che carica i dati di calorie per ogni categoria di alimento da un file Excel.
        
        :param percorso_excel: Il percorso del file Excel contenente le categorie di alimenti.
        """
        self.percorso_excel = percorso_excel
        self.alimenti = {}
        self.carica_dati()

    def carica_dati(self):
        """
        Carica i dati da tutti i fogli del file Excel. Ogni foglio rappresenta una categoria di alimenti.
        """
        # Carica il file Excel
        xls = pd.ExcelFile(self.percorso_excel)
        
        for sheet_name in xls.sheet_names:
            # Carica il contenuto del foglio come DataFrame
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Assicurati che il foglio contenga le colonne corrette
            if all(col in df.columns for col in ["tipologia_alimento", "grammi", "kcal"]):
                # Converti il DataFrame in una lista di dizionari
                categoria_alimenti = df.to_dict(orient='records')
                
                # Memorizza i dati per questa categoria (sheet)
                self.alimenti[sheet_name] = categoria_alimenti
            else:
                print(f"Attenzione: il foglio '{sheet_name}' non ha le colonne corrette.")

    def calcola_calorie(self, categoria, tipologia_alimento, grammi):
        """
        Calcola le calorie per un determinato alimento in base alla sua tipologia e quantità (in grammi).
        
        :param categoria: La categoria dell'alimento (nome dello sheet nel file Excel).
        :param tipologia_alimento: Il nome dell'alimento per cui calcolare le calorie.
        :param grammi: La quantità di alimento in grammi.
        :return: Il numero di calorie per la quantità indicata.
        """
        categoria = pulisci_stringa(categoria)
        tipologia_alimento = pulisci_stringa(tipologia_alimento)


        if categoria in self.alimenti:
            for alimento in self.alimenti[categoria]:
                if alimento['tipologia_alimento'].lower() == tipologia_alimento.lower():
                    kcal_per_grammo = alimento['kcal'] / alimento['grammi']
                    calorie_totali = kcal_per_grammo * grammi
                    return calorie_totali
        return None

    def mostra_alimenti(self):
        """
        Mostra tutti gli alimenti e le loro calorie per ciascuna categoria.
        """
        for categoria, alimenti in self.alimenti.items():
            print(f"Categoria: {categoria}")
            for alimento in alimenti:
                print(f"  - {alimento['tipologia_alimento']} ({alimento['grammi']}g): {alimento['kcal']} kcal")
                
if __name__ == "__main__":
    # Esempio di utilizzo:
    # Sostituisci con il percorso effettivo del file Excel
    percorso_excel = "data\calorie\calorie.xlsx" 
    calorie = Calorie(percorso_excel)



    # Calcola le calorie per una determinata quantità di un alimento
    categoria = "Spezie"  # Nome della categoria (sheet) dove si trova l'alimento
    alimento = "Rosmarino"  # Tipologia dell'alimento
    quantita_grammi = 150  # Quantità in grammi

    calorie_stimate = calorie.calcola_calorie(categoria, alimento, quantita_grammi)
    if calorie_stimate is not None:
        print(f"Le calorie per {quantita_grammi}g di {alimento} sono {calorie_stimate:.2f} kcal.")
    else:
        print(f"Alimento '{alimento}' non trovato nella categoria '{categoria}'.")
        # Mostra tutti gli alimenti
        calorie.mostra_alimenti()
