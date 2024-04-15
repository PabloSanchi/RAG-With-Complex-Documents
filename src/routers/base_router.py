import abc

from fastapi import APIRouter


class BaseRouter(abc.ABC):
    """Abstract class for FastAPI routers"""

    def __init__(self):
        self.router = APIRouter(prefix=self.prefix)

    @property
    @abc.abstractmethod
    def prefix(self) -> str:
        """Prefix that will precede all endpoints defined in this router."""
