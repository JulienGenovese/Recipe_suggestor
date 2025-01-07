import random
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

from Ricettario import Ricettario

class Pianificatore:
    def __init__(self, ricettario):
        self.ricettario = ricettario.ricettario
        self.piano_settimanale = None
        self.ingredienti_piano = None

    # Pianifica la settimana con i pasti per ogni giorno
    def pianifica_settimana(self):
        print("Pianificazione della settimana in corso...")
        giorni = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica']
        settimana = {}

        for giorno in giorni:
            settimana[giorno] = {
                'Pranzo': self.scegli_pasto(),
                'Cena': self.scegli_pasto()
            }
        self.piano_settimanale = settimana
        print("...COMPLETATO!")

    def lancia_moneta(self):
        esito = random.choice([True, False])
        return esito

    # Sceglie un piatto casualmente per pranzo o cena
    def scegli_pasto(self):
        esito = self.lancia_moneta()
        if esito:
            primo = random.choice(self.ricettario['primi'])
            secondo = random.choice(self.ricettario['secondi'])
            contorno = random.choice(self.ricettario['contorni'])
            piatto_unico = None
        else:
            primo = None
            secondo = None
            contorno = None
            piatto_unico = random.choice(self.ricettario['piatti_unici'])

        return {
            'Primo': primo,
            'Secondo': secondo,
            'Piatto unico': piatto_unico,
            'Contorno': contorno
        }

    # Estrae tutti gli ingredienti necessari per la settimana
    def genera_lista_ingredienti(self):
        ingredienti_totali = set()

        for giorno, pasti in self.piano_settimanale.items():
            for tipo, ricetta in pasti.items():
                for portata, info_portata in ricetta.items():
                    if info_portata is not None:
                        ingredienti_totali.update(info_portata['ingredienti'])

        self.ingredienti_piano = list(ingredienti_totali)
    
    def genera_piano_e_ingredienti(self):
        self.pianifica_settimana()
        self.genera_lista_ingredienti()


class GeneratorePiano:
    def __init__(self, pianificatore_object):
           self.pianificatore_object = pianificatore_object

    def genera_piano_e_ingredienti(self):
        self.pianificatore_object.genera_piano_e_ingredienti()

    def scrivi_piano_pdf(self, file_output):
        c = canvas.Canvas(file_output, pagesize=letter)
        width, height = letter  # dimensioni della pagina

        # Scrivere il piano settimanale
        y_position = height - 40
        c.setFont("Helvetica-Bold", 24)

        # Titolo: Piano Settimanale dei Pasti
        title = "Piano Settimanale dei Pasti"
        title_width = c.stringWidth(title, "Helvetica-Bold", 24)
        c.drawString((width - title_width) / 2, y_position, title)
        y_position -= 40  # spazio dopo il titolo

        c.setFont("Helvetica", 12)
        min_space_per_day = 180

        # Aggiungere la pianificazione dei pasti giorno per giorno
        for giorno, pasti in self.pianificatore_object.piano_settimanale.items():
            # Calcolare la larghezza del giorno
            if y_position < min_space_per_day:
                c.showPage()
                y_position = height - 40

            giorno_width = c.stringWidth(giorno.upper(), "Helvetica-Bold", 16)

            # # Impostare la posizione del rettangolo sotto il giorno
            rect_x = 25  # Lato sinistro del rettangolo
      
            rect_y = y_position - 145  # Posizione verticale per il rettangolo (sotto il giorno)

            rect_width = 560  # Larghezza rettangolo in base al testo del giorno (+20 per padding)
            rect_height = 140  # Altezza fissa del rettangolo

            # Impostare il colore di riempimento per il background
            c.setFillColor(Color(0.9, 0.9, 0.9, alpha=0.5))  # Colore grigio con opacità
            # Disegnare un rettangolo sotto il giorno
            c.rect(rect_x, rect_y, rect_width, rect_height, fill=1)

            # Giorno centrato rispetto alla pagina
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(Color(0, 0, 0))  # Impostare il colore del testo a nero
            c.drawString((width - giorno_width) / 2, y_position, f"{giorno.upper()}")
            y_position -= 25  # spazio sotto il giorno

            # Dettaglio pranzo con grassetto per "Pranzo"
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y_position, "Pranzo:")
            y_position -= 15
            c.setFont("Helvetica", 12)
            if pasti['Pranzo']['Primo']:
                c.drawString(40, y_position, f"Primo: {pasti['Pranzo']['Primo']['nome'] if pasti['Pranzo']['Primo'] else ''}")
                y_position -= 15
                c.drawString(40, y_position, f"Secondo: {pasti['Pranzo']['Secondo']['nome'] if pasti['Pranzo']['Secondo'] else ''}")
                y_position -= 15
                c.drawString(40, y_position, f"Contorno: {pasti['Pranzo']['Contorno']['nome'] if pasti['Pranzo']['Contorno'] else ''}")
            else:
                c.drawString(40, y_position, f"Piatto Unico: {pasti['Pranzo']['Piatto unico']['nome'] if pasti['Pranzo']['Piatto unico'] else ''}")
                y_position -= 30
            y_position -= 20

            # Dettaglio cena con grassetto per "Cena"
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y_position, "Cena:")
            y_position -= 15
            c.setFont("Helvetica", 12)
            if pasti['Cena']['Primo']: 
                c.drawString(40, y_position, f"Primo: {pasti['Cena']['Primo']['nome'] if pasti['Cena']['Primo'] else ''}")
                y_position -= 15
                c.drawString(40, y_position, f"Secondo: {pasti['Cena']['Secondo']['nome'] if pasti['Cena']['Secondo'] else ''}")
                y_position -= 15
                c.drawString(40, y_position, f"Contorno: {pasti['Cena']['Contorno']['nome'] if pasti['Cena']['Contorno'] else ''}")
            else:
                c.drawString(40, y_position, f"Piatto Unico: {pasti['Cena']['Piatto unico']['nome'] if pasti['Cena']['Piatto unico'] else ''}")
                y_position -= 30

            y_position -= 30  # spazio extra tra i giorni
            
            # Aggiungi una nuova pagina se necessario
            if y_position < 50:
                c.showPage()
                y_position = height - 40
            

        c.showPage()
        y_position = height - 40

        # Scrivere la lista ingredienti centrata
        c.setFont("Helvetica-Bold", 24)
        ingredients_title = "Lista Ingredienti"
        ingredients_title_width = c.stringWidth(ingredients_title, "Helvetica-Bold", 24)
        c.drawString((width - ingredients_title_width) / 2, y_position, ingredients_title)
        y_position -= 40  # spazio dopo il titolo

        # Cambia il font per la lista degli ingredienti
        c.setFont("Helvetica", 12)

        for ingrediente in self.pianificatore_object.ingredienti_piano:
            c.drawString(30, y_position, ingrediente)
            y_position -= 15
            if y_position < 50:
                c.showPage()
                y_position = height - 40

        # Salva il PDF
        c.save()

    # Scrive il piano settimanale e la lista ingredienti in un file Excel
    def scrivi_piano_excel(self, file_output):
        # Crea un DataFrame per il piano settimanale
        piano_settimanale = []
        for giorno, pasti in self.piano_settimanale.items():
            # Piano settimanale
            piano_settimanale.append({
                'Giorno': giorno,
                'Pranzo Primo': pasti['Pranzo']['Primo']['nome'] if pasti['Pranzo']['Primo'] is not None else None,
                'Pranzo Secondo': pasti['Pranzo']['Secondo']['nome'] if pasti['Pranzo']['Secondo'] is not None else None,
                'Pranzo Contorno': pasti['Pranzo']['Contorno']['nome'] if pasti['Pranzo']['Contorno'] is not None else None,
                'Pranzo Piatto Unico': pasti['Pranzo']['Piatto unico']['nome'] if pasti['Pranzo']['Piatto unico'] is not None else None,
                'Cena Primo': pasti['Cena']['Primo']['nome'] if pasti['Cena']['Primo'] is not None else None,
                'Cena Secondo': pasti['Cena']['Secondo']['nome'] if pasti['Cena']['Secondo'] is not None else None,
                'Cena Contorno': pasti['Cena']['Contorno']['nome'] if pasti['Cena']['Contorno'] is not None else None,
                'Cena Piatto Unico': pasti['Cena']['Piatto unico']['nome'] if pasti['Cena']['Piatto unico'] is not None else None,
            })
        
        df_piano_settimanale = pd.DataFrame(piano_settimanale)

        # Crea un DataFrame per gli ingredienti
        ingredienti = self.genera_lista_ingredienti()
        df_ingredienti = pd.DataFrame({'Ingredienti': ingredienti})
        # Scrive i dati in un file Excel
        with pd.ExcelWriter(file_output) as writer:
            df_piano_settimanale.to_excel(writer, sheet_name='Piano Settimanale', index=False)
            df_ingredienti.to_excel(writer, sheet_name='Ingredienti', index=False)

if __name__ == "__main__":

    # Esempio di utilizzo:
    ricette_cartella_excel = r"data/ricette"  # Sostituisci con il percorso della tua cartella
    ricettario_obj = Ricettario(ricette_cartella_excel)
    pianificatore = Pianificatore(ricettario=ricettario_obj)
    generatorepiano = GeneratorePiano(pianificatore)
    generatorepiano.genera_piano_e_ingredienti()
    # Scrivi il piano settimanale e gli ingredienti in un nuovo file Excel
    cartella_piano = r"data/pianificazione"  # Sostituisci con il percorso della tua cartella

    generatorepiano.scrivi_piano_pdf(f'{cartella_piano}/piano_settimana.pdf')

    print("Piano settimanale e ingredienti generati con successo!")