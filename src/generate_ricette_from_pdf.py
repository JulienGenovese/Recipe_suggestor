from parser.ParserStagioniNelPiatto import ParserStagioniNelPiatto
import os 

if __name__ == "__main__":
    folder_dati = r"data/ricette_to_elaborate"
    folder_dati_output = r"data/ricette"
    file_name = "Le-ricette-di-stagioni-nel-piatto-ricettario-ebook.pdf"
    parser = ParserStagioniNelPiatto(folder_dati, file_name)
    parser.estrai_dict_ricetta_from_pdf()
    parser.write_to_json(folder_dati_output)

