import streamlit as st

from chain.basic_with_history import ChatBasicWithHistoryChain


@st.cache_resource
def get_chat_chain(selected_llm: str) -> ChatBasicWithHistoryChain:
    return ChatBasicWithHistoryChain(selected_llm)