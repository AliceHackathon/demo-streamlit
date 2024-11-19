from langchain_community.embeddings import (
    HuggingFaceEmbeddings,
    HuggingFaceBgeEmbeddings,
)
from langchain_openai import OpenAIEmbeddings
from langchain_upstage import UpstageEmbeddings
from langchain_voyageai import VoyageAIEmbeddings

from config import settings

type Embeddings = (
    OpenAIEmbeddings
    | UpstageEmbeddings
    | VoyageAIEmbeddings
    | HuggingFaceEmbeddings
    | HuggingFaceBgeEmbeddings
)


def get_embeddings(embeddings_key: str) -> Embeddings:
    model_name_map = {"en": "BAAI/bge-small-en", "ko": "jhgan/ko-sbert-nli"}
    model_name = model_name_map["ko"]

    match embeddings_key:
        case "openai-2-ada":
            return OpenAIEmbeddings(
                model="text-embedding-ada-002", api_key=settings.openai_api_key
            )
        case "openai-3-small":
            return OpenAIEmbeddings(
                model="text-embedding-3-small", api_key=settings.openai_api_key
            )
        case "openai-3-large":
            return OpenAIEmbeddings(
                model="text-embedding-3-large", api_key=settings.openai_api_key
            )
        case "upstage":
            return UpstageEmbeddings(
                model="solar-embedding-1-large", api_key=settings.upstage_api_key
            )
        case ["voyage-large-2", "voyage-large-2-instruct", "voyage-multilingual-2"]:
            return VoyageAIEmbeddings(
                model=embeddings_key, api_key=settings.voyage_api_key
            )
        case "hf":
            return HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
        case "hf_bge":
            return HuggingFaceBgeEmbeddings(
                model_name=model_name,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
        case _:
            raise ValueError(f"Unknown embeddings_key: {embeddings_key}")
