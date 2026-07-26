import logging
from .base import BaseLoader
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_core.documents import Document
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

class YouTubeLoader(BaseLoader):
    def __init__(self, source: str) -> None:
        super().__init__(
            source=source,
            source_type="url",
        )

    @staticmethod
    def _extract_video_id(url: str) -> str:
        parsed = urlparse(url)

    # Standard YouTube URL
        if parsed.hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
            video_id = parse_qs(parsed.query).get("v")

            if video_id:
                return video_id[0]

            # /embed/<video_id>
            if parsed.path.startswith("/embed/"):
                return parsed.path.split("/")[2]

        # Short YouTube URL
        if parsed.hostname in {"youtu.be", "www.youtu.be"}:
            return parsed.path.lstrip("/").split("/")[0]

        raise ValueError("Invalid YouTube URL")

    @staticmethod
    def _get_transcript(video_id: str) -> str:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            transcript = " ".join(chunk["text"] for chunk in transcript_list)
            if not transcript.strip():
                raise ValueError("Transcript is empty.")
            return transcript
        except TranscriptsDisabled as e:
            logger.error("Transcript unavailable for video %s", video_id)
            raise ValueError("No transcript available for this video.") from e
        except Exception as e:
            logger.exception("Failed to fetch transcript for video %s", video_id)
            raise


    def load(self) -> list[Document]:
        video_id = self._extract_video_id(self.source)
        transcript = self._get_transcript(video_id)
        return [Document(
                        page_content=transcript,
                        metadata={
                            "source": self.source,
                            "video_id": video_id,
                            "source_type": "youtube",
                })]

        


    
