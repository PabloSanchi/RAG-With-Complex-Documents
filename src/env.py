from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Redis(BaseModel):
    host: str
    port: int
    namespace: str


class Chroma(BaseModel):
    protocol: str
    host: str
    port: int
    collection_name: str
    embedding_model: str
    dim: int


class LlamaCloud(BaseModel):
    api_key: str
    llm_model: str
    reranker: str
    timeout: int

    def get_reranker(self) -> FlagEmbeddingReranker:
        return FlagEmbeddingReranker(model=self.reranker, top_n=5)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='__')

    port: int
    llama_cloud: LlamaCloud
    chroma: Chroma
    redis: Redis


settings = Settings()
