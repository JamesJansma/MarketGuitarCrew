# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.guitarmarket.main import run
import streamlit as st



st.title('Your Guitar Price Comparison')


with st.sidebar:
    st.header('Enter FB Login')
    topic = st.text_input("Username")
    detailed_questions = st.text_input("Password", type='password')

if st.button('Run Research'):
    with st.spinner("Please wait while we gather information..."):
        run()
    st.write("Process is complete")