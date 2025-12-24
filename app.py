import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Colinde 2025", page_icon="🎄")

# 2. Link-ul tău de date
SHEET_URL = "https://docs.google.com/spreadsheets/d/10kHyUpVqxLtJ7e2cELrDtYoXd9kkiwy7cMRReaUy9Eo/export?format=csv"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(SHEET_URL)
    return df.sort_values(by='Titlu')

# Inițializăm starea paginii (pentru a ști dacă suntem în listă sau în interiorul unei colinde)
if 'colind_selectat' not in st.session_state:
    st.session_state.colind_selectat = None

try:
    df = load_data()

    # --- LOGICA DE NAVIGARE ---

    # PAGINA 2: Vizualizare Colindă
    if st.session_state.colind_selectat:
        if st.button("⬅️ Înapoi la listă"):
            st.session_state.colind_selectat = None
            st.rerun()

        colind = df[df['Titlu'] == st.session_state.colind_selectat].iloc[0]
        
        st.title(f"🎶 {colind['Titlu']}")
        st.markdown("---")

        # Media (YouTube/Dropbox)
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
        st.write("Apasă pe un titlu pentru a deschide colinda:")
        
        # Bara de căutare pentru filtrare rapidă
        search = st.text_input("🔍 Caută un titlu:", "")
        
        filtered_df = df[df['Titlu'].str.contains(search, case=False, na=False)]

        st.markdown("---")
        
        # Generăm lista de butoane (unul sub altul)
        for index, row in filtered_df.iterrows():
            if st.button(row['Titlu'], key=row['Titlu'], use_container_width=True):
                st.session_state.colind_selectat = row['Titlu']
                st.rerun()

except Exception as e:
    st.error(f"Eroare la încărcare: {e}")

st.markdown("---")
st.caption("Aplicație de Colinde - 24 Decembrie 2025")





