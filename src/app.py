import base64
import streamlit as st
import os
from Ricettario import Ricettario
from Pianificatore import GeneratorePiano, Pianificatore  

def pianifica_pasti():
    # Percorso dove si trovano le ricette
    ricette_cartella = os.path.join("data", "ricette")  # Cartella predefinita con le ricette

    # Crea il ricettario
    ricettario_obj = Ricettario(ricette_cartella)

    # Crea il pianificatore
    pianificatore = Pianificatore(ricettario=ricettario_obj)
    generatorepiano = GeneratorePiano(pianificatore)
    generatorepiano.genera_piano_e_ingredienti()
    # Pianifica i pasti per tutta la settimana

    # Percorso della cartella di pianificazione
    pianificazione_cartella = os.path.join("data", "pianificazione")

    # Scrive il piano settimanale e gli ingredienti in un file PDF
    piano_file_path = os.path.join(pianificazione_cartella, 'piano_settimana.pdf')

    # Genera il file PDF
    generatorepiano.scrivi_piano_pdf(piano_file_path)

    return piano_file_path

# Funzione per caricare un'immagine e restituire la sua stringa base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Funzione Streamlit principale
def main():
    # Carica l'immagine di sfondo
    image_path = os.path.join("data", "images", "cibo.jpg")  # Verifica il percorso
    image_base64 = get_image_as_base64(image_path)

    st.markdown("""
    <style>
        .title-description {
            position: left;
            top: 20;
            width: 100%;
            background-color: white;
            opacity: 0.9;
            padding: 50px;
            z-index: 10;
            text-align: center;
        }
        .title-description h1 {
            color: black;
            font-size: 30px;
        }
        .title-description p {
            color: black;
            font-size: 20px;
        }
    </style>
    <div class="title-description">
        <h1>PIANIFICATORE DI PASTI</h1>
        <p>Questa applicazione ti aiuta a pianificare i pasti settimanali per pranzo e cena.
        L'app utilizza le ricette pre-caricate per generare un piano settimanale e ti fornirà un file PDF con i pasti pianificati e gli ingredienti necessari.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .stApp > * {{
        opacity: 1;
    }}
    .title-description {{
        text-align: center;
        margin-top: 30px;
    }}
    .button-container {{
        text-align: center;
        margin-top: 50px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Sezione immagine e bottone
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    if st.button('Pianifica i Pasti', help="Clicca per generare il piano settimanale", key="generate_plan", use_container_width=True):
        with st.spinner("Generazione del piano settimanale..."):
            # Pianifica i pasti
            piano_file_path = pianifica_pasti()

            # Codice per il download del file
            st.download_button(
                label="Scarica il piano settimanale",
                data=open(piano_file_path, 'rb').read(),
                file_name='piano_settimana.pdf',
                mime="application/pdf"
            )

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
