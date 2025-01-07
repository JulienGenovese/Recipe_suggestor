from fuzzywuzzy import fuzz
from collections import defaultdict

# Lista di ingredienti
ingredienti = [
    "120 ml di latte",
    "300 g di tonno fresco",
    "30 g di parmigiano",
    "1 rametto di timo",
    "4 tranci di rana pescatrice",
    "qualche fogliolina di prezzemolo",
    "3 carote",
    "2 cucchiaini di miele",
    "ricotta salata a piacere",
    "150 g di fave",
    "320 g di penne integrali",
    "e sesamo",
    "basilico e erba cipollina",
    "Bucce di patate",
    "150 di pancetta in un’unica fetta",
    "80 g di piselli",
    "1 cucchiaio di bottarga",
    "1 cucchiaio di olio",
    "olio extravergine di oliva",
    "basilico",
    "catalogna",
    "2 cucchiai di senape",
    "sale",
    "altro formaggio a pasta semidura",
    "2 cetrioli",
    "200 g di farina 00",
    "70 g di bietoline",
    "2 fette sottili di scamorza affumicata o",
    "300 g di erbe cotte miste (erbette, coste, la scorza di un limone non trattato)",
    "4 rametti di timo",
    "3 uova medie",
    "2 coste di sedano",
    "olio per friggere (arachidi)",
    "210 g di riso venere",
    "100 g di rucola",
    "qualche foglia di basilico a piacere",
    "3-4 carote medie",
    "130 g di farina 00",
    "1/2 cipolla rossa",
    "1 radice di curcuma fresca o 1 cucchiaino",
    "40 g di parmigiano",
    "4 carciofi",
    "glassa di aceto balsamico",
    "2-3 cipollotti",
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
    "800 g di carote",
    "40 g di parmigiano grattugiato",
    "1 carota media",
    "pepe",
    "6 cucchiai di olio extravergine di oliva",
    "320 g di riso carnaroli",
    "12 pomodori secchi sottolio",
    "6-8 calamari medio-piccoli",
    "olio extravergine d’oliva",
    "60 g di farina",
    "un ricco mazzetto di timo, prezzemolo",
    "200 g di broccoli",
    "1 cucchiaio di grana grattugiato",
    "150 g di cavolo nero",
    "4 cucchiai di latte",
    "6 acciughe sottolio",
    "2 uova",
    "200 g di mozzarella fiordilatte",
    "20 g di uvetta",
    "40 g di gomasio",
    "un cespo di scarola",
    "4 acciughe sottolio",
    "50 g di cipolle",
    "12 cucchiai di succo di limone",
    "400 g di petto di pollo",
    "1 scalogno",
    "3 cucchiai di salsa di soia",
    "24 olive Itrane",
    "5 cucchiai di olio extravergine di oliva",
    "400 g di zucca (già pulita)",
    "di curcuma essiccata",
    "basilico fresco a piacere",
    "mezzo spicchio di aglio",
    "400 g di pomodori",
    "70 g di spinaci",
    "10 ml di aceto balsamico",
    "80 g di nocciole tostate",
    "3 cucchiai di olio extravergine di oliva",
    "un pezzetto di zenzero",
    "1 disco di pasta sfoglia",
    "70 g di farina di mais",
    "pane grattugiato",
    "1 panino da hamburger",
    "4 cucchiai di olio extravergine di oliva",
    "50 g di olive taggiasche denocciolate",
    "400 g di asparagi",
    "300 g di agretti",
    "300 g di agretti già puliti",
    "la buccia di 1/2 limone non trattato",
    "120 g di prosciutto cotto a dadini",
    "600 g di nasello in tranci",
    "50 g di stracchino",
    "1 lonza da 1 kg circa",
    "3 uova",
    "50 g di mandorle",
    "1 piadina",
    "40 g di pan grattato",
    "70 ml di olio di semi di girasole",
    "50 g di pancetta in un’unica fetta",
    "300 g di erbette",
    "280 g di pasta",
    "2 patate piccole",
    "20 g di granella di pistacchi",
    "320 g di pasta",
    "500 g di agretti",
    "2 cucchiai di semi di sesamo",
    "180 g di pomodori secchi",
    "8-10 foglie di menta fresca",
    "1 uovo",
    "250 g di nespole (peso frutto pulito)",
    "Tropea",
    "60 g di parmigiano grattugiato",
    "80 g di puntarelle",
    "80 g di pancetta",
    "1 hamburger di manzo (200 g circa)",
    "2 spicchi di aglio",
    "pepe nero",
    "700 ml di latte",
    "300 g di pane raffermo",
    "la scorza di 1 lime non trattato",
    "8 capesante",
    "2 cucchiaini di paté di pomodori secchi",
    "1 bicchiere di vino bianco",
    "qualche foglia di prezzemolo",
    "300 g di spinaci",
    "25 ml di acqua",
    "pan grattato",
    "60 g di burro",
    "qualche foglia di spinacino"
]


# Funzione per calcolare la similarità tra due ingredienti
def calcola_similarita(ingrediente1, ingrediente2):
    # Usa il fuzzy matching di fuzzywuzzy per calcolare la similarità
    return fuzz.ratio(ingrediente1.lower(), ingrediente2.lower())

# Raggruppa gli ingredienti in base alla loro similarità
def raggruppa_per_similarita(ingredienti, soglia=80):
    gruppi = defaultdict(list)
    
    for i, ingrediente1 in enumerate(ingredienti):
        trovato = False
        for gruppo in gruppi.values():
            # Se la similarità è sopra la soglia, metti l'ingrediente nel gruppo
            if any(calcola_similarita(ingrediente1, ingrediente2) > soglia for ingrediente2 in gruppo):
                gruppo.append(ingrediente1)
                trovato = True
                break
        
        # Se non è stato trovato un gruppo, crea un nuovo gruppo
        if not trovato:
            gruppi[len(gruppi)] = [ingrediente1]
    
    return gruppi

# Raggruppa gli ingredienti
gruppi_simili = raggruppa_per_similarita(ingredienti)

# Stampa i gruppi
for indice, gruppo in gruppi_simili.items():
    print(f"Gruppo {indice + 1}:")
    for ingrediente in gruppo:
        print(f" - {ingrediente}")
    print()
