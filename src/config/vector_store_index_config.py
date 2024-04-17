import sys

from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.indices.base import BaseIndex

STORAGE__EXITING___ = "Could not initialize/load the index from storage. Exiting..."


class VectorStoreIndexConfig:

    @classmethod
    def init(cls, storage_context: StorageContext) -> BaseIndex:
        """Initialize the vector store index. If the index is not found in storage, create a new one."""

        try:
            return load_index_from_storage(storage_context)
        except ValueError as err:
            if str(err) == "No index in storage context, check if you specified the right persist_dir.":
                index = VectorStoreIndex(storage_context=storage_context)
                index.storage_context.persist()
                return index
            else:
                sys.exit(STORAGE__EXITING___)
        except Exception:
            sys.exit(STORAGE__EXITING___)
