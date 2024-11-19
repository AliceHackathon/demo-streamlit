import copy

from langchain_core.documents import Document
from langchain_community.document_transformers import BeautifulSoupTransformer


class DeepBeautifulSoupTransformer:
    def __init__(self) -> None:
        self.bs_transformer = BeautifulSoupTransformer()

    def extract(self, docs: list[Document], tags_to_extract: list[str]):
        copied_docs = copy.deepcopy(docs)
        extracted_docs = self.bs_transformer.transform_documents(
            copied_docs, tags_to_extract=tags_to_extract
        )
        return extracted_docs
