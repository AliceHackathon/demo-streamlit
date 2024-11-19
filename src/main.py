import os

import yaml
from dotenv import load_dotenv
import streamlit as st


from config import settings

load_dotenv(verbose=True)

os.environ["ANTHROPIC_API_KEY"] = settings.anthropic_api_key
os.environ["OPENAI_API_KEY"] = settings.openai_api_key
os.environ["GOOGLE_API_KEY"] = settings.google_api_key
os.environ["UPSTAGE_API_KEY"] = settings.upstage_api_key
os.environ["VOYAGE_API_KEY"] = settings.voyage_api_key

os.environ["LANGCHAIN_TRACING_V2"] = settings.langchain_tracing_v2
os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint
os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project


pages = [
    st.Page("elice_pages/chat.py", title="Chat", icon="🦾"),
]


pg = st.navigation(pages)
pg.run()
