from .base import BaseLoader
from .webpage_loader import WebPageLoader
from .youtube_loader import YouTubeLoader


class LoaderFactory:

    _loaders = {
        "webpage": WebPageLoader,
        "youtube": YouTubeLoader,
    }

    @classmethod
    def create(cls, source_type: str, source: str) -> BaseLoader:
        try:
            loader_class = cls._loaders[source_type]
        except KeyError:
            raise ValueError(f"Unsupported loader type: {source_type}")

        return loader_class(source)