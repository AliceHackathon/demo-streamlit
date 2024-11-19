from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms.openllm import OpenLLM
from langchain_community.llms.vllm import VLLMOpenAI

from config import settings


type LLM = ChatOpenAI | ChatAnthropic | ChatGoogleGenerativeAI | OpenLLM | VLLMOpenAI


def get_llm(llm_key: str, remote_url: str = settings.llm_remote_server_url) -> LLM:
    hosted_model_names_map = {
        "eeve": "yanolja/EEVE-Korean-Instruct-10.8B-v1.0",
        "ko-llama3": "beomi/Llama-3-Open-Ko-8B-Instruct-preview",
        "koen-llama3": "beomi/Llama-3-KoEn-8B-Instruct-preview",
        "bllossom": "Bllossom/llama-3-Korean-Bllossom-70B",
        "bllossom-8b": "MLP-KTLim/llama-3-Korean-Bllossom-8B",
    }

    match llm_key:
        case "gpt-3.5-turbo":
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                api_key=settings.openai_api_key,
            )
        case "gpt-4o":
            return ChatOpenAI(
                model="gpt-4o", temperature=0, api_key=settings.openai_api_key
            )
        case "gpt-4o-mini":
            return ChatOpenAI(
                model="gpt-4o-mini", temperature=0, api_key=settings.openai_api_key
            )
        case "xionic":
            return ChatOpenAI(
                base_url="http://sionic.chat:8001/v1",
                api_key="934c4bbc-c384-4bea-af82-1450d7f8128d",
                model="xionic-ko-llama-3-70b",
            )
        case "openllm":
            return OpenLLM(server_url=remote_url)
        case "remote_openai":
            model_name = hosted_model_names_map["bllossom-8b"]
            return ChatOpenAI(
                openai_api_key="EMPTY",
                openai_api_base=f"{remote_url}/v1",
                model=model_name,
                # model_kwargs={"stop": ["."]},
            )
        case "vllm":
            model_name = hosted_model_names_map["bllossom-8b"]
            return VLLMOpenAI(
                openai_api_key="EMPTY",
                openai_api_base=f"{remote_url}/v1",
                model_name=model_name,
                # model_kwargs={"stop": ["."]},
            )
        case "claude-3-opus":
            return ChatAnthropic(
                model="claude-3-opus-20240229", api_key=settings.anthropic_api_key
            )
        case "claude-3-sonnet":
            return ChatAnthropic(
                model="claude-3-sonnet-20240229", api_key=settings.anthropic_api_key
            )
        case "claude-3-haiku":
            return ChatAnthropic(
                model="claude-3-haiku-20240307", api_key=settings.anthropic_api_key
            )
        case "gemini-flash":
            return ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest",
                temperature=0.0,
                api_key=settings.google_api_key,
            )
        case _:
            raise ValueError(f"Invalid llm_key: {llm_key}")
