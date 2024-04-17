from llama_index.core.indices.base import BaseIndex
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_parse import LlamaParse


class DocumentService:
    """Utility class for loading data into an index."""

    def __init__(self, parser: LlamaParse) -> None:
        self.parser = parser
        self.node_parser = MarkdownElementNodeParser(workers=8)

    async def load_data(self, document: str, index: BaseIndex) -> None:
        """Load data into the given index."""
        documents = await self.parser.aload_data(document)

        nodes = self.node_parser.get_nodes_from_documents(documents)
        base_nodes, objects = self.node_parser.get_nodes_and_objects(nodes)

        index.insert_nodes(base_nodes + objects)
        index.storage_context.persist()
