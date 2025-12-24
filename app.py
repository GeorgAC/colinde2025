import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Colinde 2025", page_icon="🎄")

# 2. Link-ul tău de date
SHEET_URL = "https://docs.google.com/spreadsheets/d/10kHyUpVqxLtJ7e2cELrDtYoXd9kkiwy7cMRReaUy9Eo/export?format=csv"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Ne asigurăm că datele sunt sortate alfabetic după Titlu
    return df.sort_values(by='Titlu')

# Folosim ID-ul unic pentru navigare
if 'id_selectat' not in st.session_state:
    st.session_state.id_selectat = None

try:
    df = load_data()

    # PAGINA 2: Vizualizare Colindă
    if st.session_state.id_selectat is not None:
        if st.button("⬅️ Înapoi la listă"):
            st.session_state.id_selectat = None
            st.rerun()

        # Căutăm colinda după ID-ul unic, nu după Titlu
        colind = df[df['ColindID'] == st.session_state.id_selectat].iloc[0]
        
        st.title(f"🎶 {colind['Titlu']}")
        st.markdown("---")

        # Player Video/Audio
        link = str(colind['Link'])
        if "youtube.com" in link or "youtu.be" in link:
            st.video(link)
        elif "dropbox.com" in link:
            direct_link = link.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("?dl=0", "")
            st.audio(direct_link)

        st.subheader("Versuri")
        st.text(colind['Versuri'])

    # PAGINA 1: Lista Completă
    else:
        st.title("🎄 Toate Colindele")
        search = st.text_input("🔍 Caută un colind:", "")
        
        filtered_df = df[df['Titlu'].str.contains(search, case=False, na=False)]

        st.markdown("---")
        
        # Generăm lista de butoane folosind ColindID ca cheie unică
        for index, row in filtered_df.iterrows():
            # Cheia este acum "ID_Titlu" pentru a fi 100% unică
            button_key = f"{row['ColindID']}_{row['Titlu']}"
            if st.button(row['Titlu'], key=button_key, use_container_width=True):
                st.session_state.id_selectat = row['ColindID']
                st.rerun()

except Exception as e:
    st.error(f"Eroare: {e}")
    st.info("Verifică dacă ai adăugat coloana 'ColindID' în tabelul Google Sheets.")

st.markdown("---")
st.caption("Aplicație de Colinde - 24 Decembrie 2025")







