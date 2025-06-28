from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class VideoResponse(BaseModel):
    id: str = Field(..., description="Video ID")
    title: str = Field(..., description="Video title")
    transcript: str = Field(..., description="Video transcript")
    tags: List[str] = Field(..., description="Generated tags")
    created_at: datetime = Field(..., description="Upload timestamp")
    download_url: Optional[str] = Field(None, description="Direct download URL for the video")

class SearchResponse(BaseModel):
    videos: List[VideoResponse] = Field(..., description="List of videos")
    total: int = Field(..., description="Total number of videos found")

class VideoUploadResponse(BaseModel):
    message: str = Field(..., description="Upload status message")
    video: VideoResponse = Field(..., description="Uploaded video details")

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message") 