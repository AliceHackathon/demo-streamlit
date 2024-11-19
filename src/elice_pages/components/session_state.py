from typing import Literal
import uuid

from pydantic import BaseModel
import streamlit as st
from streamlit.runtime.state.session_state_proxy import SessionStateProxy
from langchain_core.documents import Document


class SessionChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = ""
    emotion: str = ""
    with_source: bool = False
    metadata: list[Document] = []
    error: str = ""

    @staticmethod
    def create_start_message() -> "SessionChatMessage":
        return SessionChatMessage(
            role="assistant",
            content="안녕하세요! 무엇이든 물어보세요 😊",
        )

    def display_sources(self, display_details: bool = False):
        sources = set(
            [
                f"[{doc.metadata['source_title']}]({doc.metadata['source']})"
                for doc in self.metadata
            ]
        )

        if display_details:
            # TODO: should fix this to remove duplicated documents
            for doc in self.metadata:
                with st.expander(source):
                    st.write(doc.page_content)
                    with st.container(border=True):
                        st.json(doc.metadata)
        else:
            source_with_number = [
                f"{idx}. {source}" for idx, source in enumerate(sources, 1)
            ]

            st.markdown(
                "Please refer to the following links if you want more information:"
            )
            for source in source_with_number:
                st.markdown(source)

    def display(self, display_details: bool = False):
        avatar = "🤖" if self.role == "assistant" else "🙋‍♂️"
        with st.chat_message(self.role, avatar=avatar):
            st.markdown(self.content)
            st.markdown(self.emotion)

            if self.error != "":
                st.exception(self.error)

            # if self.with_source:
            #     self.display_sources(display_details)


class SessionState(SessionStateProxy):
    def __init__(self) -> None:
        super().__init__()

        if "messages" not in st.session_state:
            self.messages = [SessionChatMessage.create_start_message()]

        if "session_id" not in st.session_state:
            self.session_id = str(uuid.uuid4())

    def display_all_messages(self, display_details: bool = False):
        for message in self.messages:
            message.display(display_details)

    def append_message(
        self, message: SessionChatMessage, display_details: bool = False
    ):
        message.display(display_details)
        self.messages.append(message)

    def clear_messages(self):
        self.messages = [SessionChatMessage.create_start_message()]
