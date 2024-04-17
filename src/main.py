import nest_asyncio
import uvicorn
from config.llama_index_config import LlamaIndexConfig
from config.vector_store_index_config import VectorStoreIndexConfig
from env import settings
from fastapi import FastAPI
from llama_index.core import StorageContext
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.indices.base import BaseIndex
from llama_index.core.storage.index_store.keyval_index_store import KVIndexStore
from llama_index.core.vector_stores.types import BasePydanticVectorStore
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.storage.index_store.redis import RedisIndexStore
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_parse import LlamaParse

from src.routers.chat_router import ChatRouter
from src.routers.ingest_router import IngestRouter
from src.services.document_service import DocumentService


class Main:
    @classmethod
    def bootstrap(cls) -> None:
        nest_asyncio.apply()
        uvicorn.run(
            cls._generate_app(),
            host="0.0.0.0",
            port=settings.port,
            loop="asyncio"
        )

    @classmethod
    def _generate_app(cls) -> FastAPI:
        app: FastAPI = FastAPI(title="Retrieval-Augmented Generation With Complex Documents", version="0.0.1")

        LlamaIndexConfig.init()

        chroma_store: BasePydanticVectorStore = ChromaVectorStore(
                host=settings.chroma.host,
                port=settings.chroma.port,
                collection_name=settings.chroma.collection_name
        )

        index_store: KVIndexStore = RedisIndexStore.from_host_and_port(
            host=settings.redis.host,
            port=settings.redis.port,
            namespace=settings.redis.namespace
        )

        storage_context: StorageContext = StorageContext.from_defaults(
            vector_store=chroma_store,
            index_store=index_store
        )

        index: BaseIndex = VectorStoreIndexConfig.init(storage_context)

        reranker: FlagEmbeddingReranker = settings.llama_cloud.get_reranker()
        streaming_query_engine: BaseQueryEngine = index.as_query_engine(
            streaming=True,
            similarity_top_k=3,
            node_postprocessors=[reranker]
        )

        parser = LlamaParse(
            api_key=settings.llama_cloud.api_key,
            result_type="markdown",
            num_workers=4,
            verbose=True,
            language="en"
        )

        app.include_router(ChatRouter(streaming_query_engine).router)
        app.include_router(IngestRouter(index, DocumentService(parser)).router)

        return app


if __name__ == "__main__":
    Main.bootstrap()
