import streamlit as st
import pandas as pd

st.set_page_config(page_title="Colinde 2025", page_icon="🎄")

# Link-ul tău de Google Sheets (format CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/10kHyUpVqxLtJ7e2cELrDtYoXd9kkiwy7cMRReaUy9Eo/export?format=csv"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(SHEET_URL)
    return df.sort_values(by='Titlu')

st.title("🎶 Colinde de Crăciun")

try:
    df = load_data()
    search = st.text_input("Caută colindul:", "")
    filtered_df = df[df['Titlu'].str.contains(search, case=False, na=False)]

    titlu_ales = st.selectbox("Alege colindul:", filtered_df['Titlu'].unique())

    if titlu_ales:
        colind = df[df['Titlu'] == titlu_ales].iloc[0]
        st.header(colind['Titlu'])

        # Media integrată
        link = str(colind['Link'])
        if "youtube.com" in link or "youtu.be" in link:
            st.video(link)
        elif "dropbox.com" in link:
            direct_link = link.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("?dl=0", "")
            st.audio(direct_link)

        st.subheader("Versuri")
        st.text(colind['Versuri'])
except:
    st.error("Verifică dacă tabelul Google Sheets este public (Anyone with link)!")


