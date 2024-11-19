from operator import itemgetter
from typing import Optional

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables.history import RunnableWithMessageHistory

from config import settings
from core.memory.session import SessionInMemory
from core.qdrant import QdrantClient
from core.llms import get_llm
from chain.prompts import chat_prompt_with_history_and_emotion


from typing_extensions import Annotated, TypedDict


class EmotionalResponse(TypedDict):
    """Emotional response. It's a response that includes the response and the relatedemotion."""

    response: Annotated[str, ..., "The response of the chat"]
    emotion: Annotated[
        str,
        ...,
        "The emotion of the chat. It should be one of 'happy', 'sad', 'neutral', 'angry', 'surprised', 'disgusted', 'fearful', 'disappointed'",
    ]


class ChatBasicWithHistoryChain:
    vectorstore_collection_prefix: str = "elice_chat"

    def __init__(self, llm_key: str = "gpt-4o-mini") -> None:
        llm = get_llm(llm_key)

        session_memory = SessionInMemory()

        structured_llm = llm.with_structured_output(EmotionalResponse)

        self.simple_chain = (
            itemgetter("question")
            | chat_prompt_with_history_and_emotion
            | structured_llm
        )

        self.chain_with_history = RunnableWithMessageHistory(
            chat_prompt_with_history_and_emotion
            | structured_llm,
            session_memory.get_session_history,
            input_messages_key="question",
            history_messages_key="history",
        )

    def invoke(self, question: str, session_id: str) -> EmotionalResponse:
        response = self.chain_with_history.invoke(
            {"question": question},
            config={"configurable": {"session_id": session_id}},
        )

        return response

    # def invoke(self, question: str, session_id: str) -> str:
    #     response = self.simple_chain.invoke(
    #         question,
    #         config={"configurable": {"session_id": session_id}},
    #     )

    #     return response
