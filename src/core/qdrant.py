from langchain_core.documents import Document

# from langchain_qdrant import QdrantVectorStore
# from langchain_qdrant import Qdrant

from langchain_community.vectorstores.qdrant import Qdrant
import qdrant_client

from core.embeddings import get_embeddings
from config import settings


class QdrantClient:
    def __init__(
        self, url: str = settings.qdrant_url, embedding_key: str = "openai-2-ada"
    ):
        self.url = url
        self.embeddings = get_embeddings(embedding_key)

    def build(self, documents: list[Document], collection_name: str) -> Qdrant:
        db = Qdrant.from_documents(
            documents, self.embeddings, url=self.url, collection_name=collection_name
        )
        return db

    def load(self, collection_name: str) -> Qdrant:
        # db = QdrantVectorStore.from_existing_collection(
        #     collection_name=collection_name, embedding=self.embeddings, url=self.url
        # )
        client = qdrant_client.QdrantClient(url=self.url)
        db = Qdrant(
            client=client, collection_name=collection_name, embeddings=self.embeddings
        )
        return db
