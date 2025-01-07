import re
from collections import defaultdict
from fuzzywuzzy import fuzz

class Ingredienti:
    def __init__(self):
        self.ingredienti = defaultdict(float)

    def aggiungi(self, ingrediente: str):
        """Aggiungi un ingrediente con la quantità alla lista"""
        # Regex per identificare la quantità e l'ingrediente (gestisce g, kg, etc.)
        match = re.match(r"(\d+\.?\d*)\s*(\w+|\D+)(?:\s*(g|kg|ml|l|fetta|foglia|pz|noce|spicchio|rametto)?)", ingrediente.lower())
        
        if match:
            quantita = float(match.group(1))  # Quantità
            nome = match.group(2).strip()  # Nome dell'ingrediente
            unita = match.group(3) if match.group(3) else 'pz'  # Unità di misura (default 'pz' se non specificata)
            
            # Convertire unità di misura in grammi o millilitri dove possibile
            if unita in ['kg', 'g']:
                # Passa tutto in grammi (g)
                if unita == 'kg':
                    quantita *= 1000  # Converte kg in g
                self.ingredienti[nome] += quantita
            elif unita in ['l', 'ml']:
                # Passa tutto in millilitri (ml)
                if unita == 'l':
                    quantita *= 1000  # Converte litri in ml
                self.ingredienti[nome] += quantita
            else:
                # Per gli altri ingredienti (pz, noce, foglia, ecc), trattiamo come unità base
                self.ingredienti[nome] += quantita
        else:
            print(f"Impossibile riconoscere l'ingrediente: {ingrediente}")

    def somma_ingredienti(self):
        """Restituisce la lista degli ingredienti raggruppati con le quantità totali"""
        ingredienti_raggruppati = []
        for nome, quantita in self.ingredienti.items():
            ingredienti_raggruppati.append(f"{quantita:.2f} {nome}")
        return ingredienti_raggruppati

    def calcola_similarita(self, ingrediente1: str, ingrediente2: str):
        """Calcola la similarità tra due ingredienti usando fuzzywuzzy"""
        return fuzz.ratio(ingrediente1.lower(), ingrediente2.lower())

    def raggruppa_simili(self, soglia=80):
        """Raggruppa gli ingredienti simili e somma le quantità"""
        gruppi = defaultdict(list)
        ingredienti_da_raggruppare = list(self.ingredienti.items())
        
        for i, (nome1, quantita1) in enumerate(ingredienti_da_raggruppare):
            trovato = False
            for nome_gruppo, gruppo in gruppi.items():
                if any(self.calcola_similarita(nome1, nome2) > soglia for nome2, _ in gruppo):
                    gruppo.append((nome1, quantita1))
                    trovato = True
                    break
            
            if not trovato:
                gruppi[nome1].append((nome1, quantita1))
        
        # Somma le quantità per ogni gruppo
        ingredienti_raggruppati = defaultdict(float)
        for gruppo in gruppi.values():
            for nome, quantita in gruppo:
                ingredienti_raggruppati[nome] += quantita
        
        return ingredienti_raggruppati

# Esempio di utilizzo
if __name__ == "__main__":
    ingredienti_lista = [
        "2 noci di burro",
        "farina di farro per infarinare il pollo",
        "250 g di piselli già lessati",
        "qualche foglia di basilico",
        "100 g di scamorza affumicata",
        "9 sfoglie di lasagne secche o fresche",
        "100 g di olio di semi di girasole",
        "noce moscata",
        "1 spicchio di aglio",
        "40 g di pinoli",
        "un mazzetto di prezzemolo",
        "semi misti per decorare",
        "300 g di zucca",
        "15 g di pomodori secchi sottolio",
        "7 g di zucchero",
        "80 g di provolone calabrese",
        "250 g di ricotta",
        "15 g di noci",
        "800 g di carote"
    ]

    # Crea la classe Ingredienti e aggiungi gli ingredienti
    ingredienti_obj = Ingredienti()
    for ingrediente in ingredienti_lista:
        ingredienti_obj.aggiungi(ingrediente)

    # Raggruppa gli ingredienti simili e somma le quantità
    ingredienti_raggruppati = ingredienti_obj.raggruppa_simili()

    # Mostra gli ingredienti raggruppati
    print("Ingredienti raggruppati con le quantità totali:")
    for nome, quantita in ingredienti_raggruppati.items():
        print(f"{quantita:.2f} {nome}")
