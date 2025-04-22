import os
from guitarmarket.main import run

os.system("playwright install chromium")

# Handle SQLite for ChromaDB
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except (ImportError, KeyError):
    pass

import sys
import streamlit as st



st.title('Your Guitar Price Comparison')


with st.sidebar:
    st.header('Enter FB Login')
    topic = st.text_input("Username")
    detailed_questions = st.text_input("Password", type='password')

if st.button('Run Research'):
    