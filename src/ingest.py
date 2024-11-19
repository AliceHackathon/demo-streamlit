from itertools import chain

from data.ingest_manager import DataIngestManager
from data.urls import TOTAL_URLS


def ingest():
    manager = DataIngestManager()

    flatten_urls = list(chain.from_iterable(TOTAL_URLS.values()))
    manager.execute(flatten_urls)


if __name__ == "__main__":
    ingest()
