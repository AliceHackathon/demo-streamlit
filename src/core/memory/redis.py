import os
from langchain_community.chat_message_histories import RedisChatMessageHistory


REDIS_URL = os.getenv("REDIS_URL")


class RedisMemory:
    def __init__(self, url: str = REDIS_URL) -> None:
        self.url = url

    def get_message_history(self, session_id: str) -> RedisChatMessageHistory:
        return RedisChatMessageHistory(session_id, url=self.url)
