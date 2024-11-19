from pydantic.v1 import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Change all fields to lower case
class Settings(BaseSettings):
    ##### GENERAL #####
    enable_sidebar_selectboxes: bool = Field(default=True)

    ##### LLM API KEYS #####
    anthropic_api_key: str = Field()
    openai_api_key: str = Field()
    google_api_key: str = Field()
    upstage_api_key: str = Field()
    voyage_api_key: str = Field()

    ##### LANGSMITH #####
    langchain_tracing_v2: str = Field("true")
    langchain_api_key: str = Field()
    langchain_endpoint: str = Field("https://api.smith.langchain.com")
    langchain_project: str = Field()

    ##### REMOTE LLM #####
    llm_remote_server_url: str = Field()
    llm_api_key: str = Field()

    ##### DB #####
    redis_url: str = Field("http://localhost:6379")
    qdrant_url: str = Field("http://elice-qdrant:6333")
    collection_version: str = Field("v1")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings(_env_file=".env")
