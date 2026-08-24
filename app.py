import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

# Configuration de la page
st.set_page_config(
    page_title="Agenda de Sommeil",
    page_icon="😴",
    layout="centered"
)

st.title("😴 Agenda de Sommeil")
st.caption("Suivi de la qualité de sommeil ressentie – inspiré du Réseau Morphée")

# --- Formulaire de saisie ---
st.header("Nouvelle nuit")

with st.form("nouvelle_nuit", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        date_nuit = st.date_input("Date de la nuit (du ... au ...)", value=date.today())
        heure_coucher = st.time_input("Heure de coucher", value=None)
        heure_lever = st.time_input("Heure de lever", value=None)
    
    with col2:
        qualite_sommeil = st.selectbox(
            "Qualité du sommeil",
            ["TB", "B", "Moy", "M", "TM"],
            index=2
        )
        qualite_reveil = st.selectbox(
            "Qualité du réveil",
            ["TB", "B", "Moy", "M", "TM"],
            index=2
        )
        forme_journee = st.selectbox(
            "Forme pendant la journée",
            ["TB", "B", "Moy", "M", "TM"],
            index=2
        )
    
    traitements = st.text_input("Traitements")
    remarques = st.text_area("Remarques particulières")
    
    submitted = st.form_submit_button("Enregistrer la nuit")

# --- Sauvegarde ---
DATA_FILE = "data/sommeil.csv"

if submitted:
    # Création du dossier data s'il n'existe pas
    os.makedirs("data", exist_ok=True)
    
    nouvelle_ligne = {
        "date": date_nuit,
        "heure_coucher": heure_coucher.strftime("%H:%M") if heure_coucher else "",
        "heure_lever": heure_lever.strftime("%H:%M") if heure_lever else "",
        "qualite_sommeil": qualite_sommeil,
        "qualite_reveil": qualite_reveil,
        "forme_journee": forme_journee,
        "traitements": traitements,
        "remarques": remarques,
        "enregistre_le": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    # Ajout au CSV
    df_new = pd.DataFrame([nouvelle_ligne])
    
    if os.path.exists(DATA_FILE):
        df_new.to_csv(DATA_FILE, mode="a", header=False, index=False)
    else:
        df_new.to_csv(DATA_FILE, index=False)
    
    st.success("Nuit enregistrée avec succès !")

# --- Affichage de l'historique ---
st.header("Historique")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.dataframe(df, use_container_width=True)
    
    # Bouton d'export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Télécharger le CSV",
        data=csv,
        file_name="agenda_sommeil.csv",
        mime="text/csv"
    )
else:
    st.info("Aucune nuit enregistrée pour le moment.")
