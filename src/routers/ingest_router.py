import shutil
import tempfile

from fastapi import UploadFile
from fastapi.responses import JSONResponse
from llama_index.core.indices.base import BaseIndex

from ..services.document_service import DocumentService
from .base_router import BaseRouter


class IngestRouter(BaseRouter):
    prefix: str = "/ingest"

    def __init__(self, index: BaseIndex, document_service: DocumentService):
        super().__init__()
        self.index = index
        self.document_service = document_service

        self.router.add_api_route(
            '/document',
            self.add_document,
            methods=['POST'],
            description='Add a document to the index'
        )

    async def add_document(self, file: UploadFile) -> JSONResponse: # Annotated[bytes, File()]
        """Add a document to the index."""

        temp = tempfile.NamedTemporaryFile(delete=True, suffix=".pdf")
        shutil.copyfileobj(file.file, temp)

        try:
            self.document_service.load_data(temp.name, self.index)
        except Exception as e:
            return JSONResponse(status_code=400, content={'message': f'Error: {e}'})
        finally:
            temp.flush()
            temp.close()

        return JSONResponse(status_code=200, content={'message': 'Document added successfully'})
