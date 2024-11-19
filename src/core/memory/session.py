from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


class SessionInMemory:
    store: dict
    """In-memory storage for session history."""

    def __init__(self) -> None:
        self.store = {}

    def get_session_history(self, session_ids: str) -> BaseChatMessageHistory:
        print(session_ids)
        if session_ids not in self.store:
            self.store[session_ids] = ChatMessageHistory()

        print(f"history :: {self.store[session_ids]}")
        return self.store[session_ids]
