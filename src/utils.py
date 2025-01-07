import re

def pulisci_stringa(input_string):
    """
    Pulizia di una stringa:
    - Rimuove gli spazi iniziali e finali.
    - Rimuove caratteri speciali (eccetto lettere, numeri e spazi).
    - Rimuove spazi duplicati.
    - Converte la stringa in minuscolo (opzionale).
    
    :param input_string: La stringa di input da pulire.
    :return: La stringa pulita.
    """
    # Rimuove gli spazi iniziali e finali
    input_string = input_string.strip()

    # Rimuove tutti i caratteri non alfanumerici e non spazi
    input_string = re.sub(r'[^a-zA-Z0-9\s]', '', input_string)
    
    # Rimuove spazi duplicati (più di uno) e li sostituisce con un singolo spazio
    input_string = re.sub(r'\s+', ' ', input_string)
    
    # Opzionale: Converte la stringa in minuscolo
    input_string = input_string.lower()
    
    return input_string

if __name__ == "__main__":
    # Esempio di utilizzo
    input_string = "   Ciao!! Questo è un  esempio... di    stringa  !! "
    stringa_pulita = pulisci_stringa(input_string)
    print(stringa_pulita)  # Uscita: "ciao questo è un esempio di stringa"
