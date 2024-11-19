from typing import List

from pydantic import BaseModel
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage


def format_messages(messages: list[BaseMessage]) -> str:
    return "\n".join(message.content for message in messages)


def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def add_metadata_in_answer(answer: str, docs: list[Document]) -> str:
    source_data = set(
        [f"[{doc.metadata['source_title']}]({doc.metadata['source']})" for doc in docs]
    )
    source_markdowns = "\n\n".join(
        [f"{idx}. {data}" for idx, data in enumerate(source_data, 1)]
    )

    if len(source_data) == 0:
        return answer

    return f"""{answer}

Please refer to the following links if you want more information:

{source_markdowns}
    """


class AnswerWithSource(BaseModel):
    answer: str
    context: List[Document]
