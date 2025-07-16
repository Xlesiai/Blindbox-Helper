# --------Imports--------
import streamlit as st
import json
from scripts import scrapper

# --------Data--------
note_items: dict = {}


st.title("Rednote Scrapper")
st.write("I am making this so that i can webscrape labubu one piece info from rednote. :)")

# Scrape
with st.expander("Scrape"):
    query = st.text_input("Query", 'Labubu One Piece Weights')

    if st.button("Scrape"):
        # Scraping code here...
        st.write("Scraping...")
        scrapper.scrape(query, note_items)

# Display results
with st.expander("Results"):
    note_items = st.file_uploader("Upload", type=["json"])
    if not note_items:
        note_items = {}
    st.text_area('', note_items)
    st.download_button("Download", json.dumps(note_items), 'results.json')
