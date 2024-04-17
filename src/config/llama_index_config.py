from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

from src.env import settings


class LlamaIndexConfig:
    """Initializes the Llama Index llm and embedding configuration."""

    @classmethod
    def init(cls) -> None:
        llm = Ollama(model=settings.llama_cloud.llm_model, request_timeout=settings.llama_cloud.timeout)
        embedding_model = HuggingFaceEmbedding(model_name=settings.chroma.embedding_model)

        Settings.llm = llm
        Settings.embed_model = embedding_model
