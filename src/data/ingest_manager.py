from typing import Iterator

from tqdm.auto import tqdm
from loguru import logger

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader


from config import settings
from core.qdrant import QdrantClient
from data.data_processor.deep_beautiful_soup_transformer import (
    DeepBeautifulSoupTransformer,
)


class DataIngestManager:
    def __init__(
        self,
        url: str,
        embedding_key: str = "openai-2-ada",
        version: str = settings.collection_version,
    ) -> None:
        self.bs_transformer = DeepBeautifulSoupTransformer()
        self.splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=3000, chunk_overlap=0
        )

        self.qdrant_client = QdrantClient(url=url, embedding_key=embedding_key)
        self.qdrant_collection_name = f"visaflo_guide_{embedding_key}_{version}"

    def _load_urls(self, urls: list[str]) -> Iterator[Document]:
        logger.info("STARTING SCRAPING")

        loader = AsyncChromiumLoader(urls)

        return loader.lazy_load()

    def _extract(self, docs: list[Document]) -> list[Document]:
        logger.info("STARTING TRANSFORMING")

        titles = self.bs_transformer.extract(docs, tags_to_extract=["title"])
        extracted_docs = self.bs_transformer.extract(
            docs, tags_to_extract=["div", "h1", "p", "li", "a", "span"]
        )

        for title, doc in zip(titles, extracted_docs):
            doc.metadata["source_title"] = title.page_content

        return extracted_docs

    def _split(self, docs: list[Document]) -> list[Document]:
        logger.info("STARTING SPLITTING")

        return self.splitter.split_documents(docs)

    def _ingest(self, docs: list[Document]) -> None:
        logger.info("STARTING INGESTING")

        self.qdrant_client.build(docs, self.qdrant_collection_name)

    def execute(self, urls: list[str]) -> list[Document]:
        docs = self._load_urls(urls)

        loaded_docs = []
        for doc in tqdm(docs, desc="Load Documents"):
            logger.info(f"Loaded {doc.url}")
            loaded_docs.append(doc)

        extracted_docs = self._extract(loaded_docs)
        splits = self._split(extracted_docs)
        self._ingest(splits)
