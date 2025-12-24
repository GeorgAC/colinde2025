import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Colinde 2025", page_icon="🎄")

# 2. Link-ul tău de date (formatul de export CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/10kHyUpVqxLtJ7e2cELrDtYoXd9kkiwy7cMRReaUy9Eo/export?format=csv"

@st.cache_data(ttl=600)
def load_data():
    # Citim datele și le sortăm alfabetic după Titlu
    df = pd.read_csv(SHEET_URL)
    return df.sort_values(by='Titlu')

try:
    df = load_data()

    st.title("🎶 Colecția de Colinde")
    st.markdown("---")

    # --- AICI ESTE MODIFICAREA DE ORDINE ---

    # 1. Alege colindul (Lista completă alfabetică)
    toate_titlurile = df['Titlu'].unique()
    titlu_ales = st.selectbox("Alege colindul din listă:", toate_titlurile)

    # 2. Caută colindul (Bara de căutare dedesubt)
    search = st.text_input("Sau caută rapid un titlu:", "")

    # --- LOGICA DE AFIȘARE ---

    # Dacă utilizatorul scrie ceva în căutare, prioritizăm căutarea
    if search:
        rezultate = df[df['Titlu'].str.contains(search, case=False, na=False)]
        if not rezultate.empty:
            # Luăm primul rezultat din căutare dacă utilizatorul scrie activ
            colind_final = rezultate.iloc[0]
        else:
            st.warning("Nu am găsit colindul căutat. Folosește lista de mai sus.")
            colind_final = df[df['Titlu'] == titlu_ales].iloc[0]
    else:
        # Altfel, afișăm ce este selectat în listă
        colind_final = df[df['Titlu'] == titlu_ales].iloc[0]

    # Afișarea propriu-zisă
    st.markdown(f"## {colind_final['Titlu']}")
    
    # Video/Audio Player
    link = str(colind_final['Link'])
    if "youtube.com" in link or "youtu.be" in link:
        st.video(link)
    elif "dropbox.com" in link:
        direct_link = link.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("?dl=0", "")
        st.audio(direct_link)

    # Versuri cu formatarea din Excel
    st.subheader("Versuri")
    st.text(colind_final['Versuri'])

except Exception as e:
    st.error(f"Eroare la încărcare. Verifică dacă tabelul este public! Detalii: {e}")

st.markdown("---")
st.caption("Aplicație de Colinde - Crăciun 2025")





