from llama_index.core.base.base_query_engine import BaseQueryEngine
from sse_starlette.sse import EventSourceResponse

from .base_router import BaseRouter


class ChatRouter(BaseRouter):
    prefix: str = "/chat"

    def __init__(self, query_engine: BaseQueryEngine):
        super().__init__()
        self.query_engine: BaseQueryEngine = query_engine

        self.router.add_api_route(
            '/ask',
            self.chat,
            methods=['GET'],
            description="Ask a question and get a streamed response."
        )

    async def chat(self, query: str) -> EventSourceResponse:
        stream = self.query_engine.query(query).response_gen
        return EventSourceResponse(stream)
