import streamlit as st


def select_embedding(
    label: str = "Choose Embeddings", default: str = "voyage-multilingual-2"
):
    options = [
        "openai-2-ada",
        "openai-3-small",
        "openai-3-large",
        "upstage",
        "voyage-large-2",
        "voyage-large-2-instruct",
        "voyage-multilingual-2",
        "hf",
        "hf_bge",
    ]
    default_idx = options.index(default)

    selected_embedding = st.sidebar.selectbox(
        label, options, index=default_idx, placeholder="Choose Embeddings"
    )
    return selected_embedding


def select_llm(label: str = "Choose LLM", default: str = "gpt-4o-mini"):
    options = [
        "gpt-3.5-turbo",
        "gpt-4o",
        "gpt-4o-mini",
        "claude-3-opus",
        "claude-3-sonnet",
        "claude-3-haiku",
        "gemini-flash",
        "xionic",
        "openllm",
        "remote_openai",
        "vllm",
    ]
    default_idx = options.index(default)

    selected_llm = st.sidebar.selectbox(
        label, options, index=default_idx, placeholder="Choose LLM"
    )
    return selected_llm


def select_chain(label: str = "Choose type of LLM Chain", default: str = "basic"):
    options = ["basic", "hyde", "multi_query", "basic_memory_attached"]
    default_idx = options.index(default)
    selected_chain = st.sidebar.selectbox(
        label, options, index=default_idx, placeholder="Choose type of LLM Chain"
    )
    return selected_chain
