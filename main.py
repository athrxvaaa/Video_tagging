from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from bson import ObjectId
import os
import io
from datetime import datetime
from typing import Optional, List
import logging

# Import our modules
from config import settings
from models import VideoResponse, SearchResponse
from database import db
from services import video_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    db.close()

@app.post("/upload", response_model=VideoResponse)
async def upload_video(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None)
):
    """Upload a video file and generate tags"""
    
    # Validate file type
    if not file.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")
    
    # Read file data
    video_data = await file.read()
    
    # Check file size
    if len(video_data) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size must be under 100MB")
    
    try:
        # Get database instances
        database = db.get_db()
        fs = db.get_fs()
        
        # Store video in GridFS
        file_id = fs.put(
            io.BytesIO(video_data),
            filename=file.filename,
            content_type=file.content_type
        )
        
        # Extract transcript
        transcript = video_service.extract_transcript(video_data)
        
        # Generate title using ChatGPT (ignore manual title for now)
        video_title = video_service.generate_title_from_transcript(transcript, file.filename)
        
        # Extract tags
        tags = video_service.extract_tags(transcript, file.filename)
        
        # Store metadata in videos collection
        video_doc = {
            "file_id": file_id,
            "title": video_title,
            "transcript": transcript,
            "tags": tags,
            "created_at": datetime.utcnow()
        }
        
        result = database.videos.insert_one(video_doc)
        
        return VideoResponse(
            id=str(result.inserted_id),
            title=video_title,
            transcript=transcript,
            tags=tags,
            created_at=video_doc["created_at"],
            download_url=f"/video/{result.inserted_id}"
        )
        
    except Exception as e:
        logger.error(f"Error uploading video: {e}")
        raise HTTPException(status_code=500, detail="Error uploading video")

@app.get("/search", response_model=SearchResponse)
async def search_videos(query: str):
    """Search videos by tags and transcript"""
    
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    try:
        database = db.get_db()
        
        # Create text search query
        search_query = {
            "$or": [
                {"tags": {"$regex": query, "$options": "i"}},
                {"transcript": {"$regex": query, "$options": "i"}},
                {"title": {"$regex": query, "$options": "i"}}
            ]
        }
        
        # Find videos
        cursor = database.videos.find(search_query).sort("created_at", -1)
        videos = list(cursor)
        
        # Convert to response format
        video_responses = []
        for video in videos:
            video_responses.append(VideoResponse(
                id=str(video["_id"]),
                title=video["title"],
                transcript=video["transcript"],
                tags=video["tags"],
                created_at=video["created_at"],
                download_url=f"/video/{video['_id']}"
            ))
        
        return SearchResponse(
            videos=video_responses,
            total=len(video_responses)
        )
        
    except Exception as e:
        logger.error(f"Error searching videos: {e}")
        raise HTTPException(status_code=500, detail="Error searching videos")

@app.get("/video/{video_id}")
async def get_video(video_id: str):
    """Stream video file by ID"""
    
    try:
        database = db.get_db()
        fs = db.get_fs()
        
        # Find video metadata
        video_doc = database.videos.find_one({"_id": ObjectId(video_id)})
        if not video_doc:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Get file from GridFS
        grid_out = fs.get(video_doc["file_id"])
        
        # Create streaming response
        def iterfile():
            yield from grid_out
        
        return StreamingResponse(
            iterfile(),
            media_type=grid_out.content_type,
            headers={"Content-Disposition": f"attachment; filename={grid_out.filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error retrieving video: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving video")

@app.get("/videos", response_model=List[VideoResponse])
async def list_videos(limit: int = 10, offset: int = 0):
    """List all videos with pagination"""
    
    try:
        database = db.get_db()
        
        cursor = database.videos.find().sort("created_at", -1).skip(offset).limit(limit)
        videos = list(cursor)
        
        video_responses = []
        for video in videos:
            video_responses.append(VideoResponse(
                id=str(video["_id"]),
                title=video["title"],
                transcript=video["transcript"],
                tags=video["tags"],
                created_at=video["created_at"],
                download_url=f"/video/{video['_id']}"
            ))
        
        return video_responses
        
    except Exception as e:
        logger.error(f"Error listing videos: {e}")
        raise HTTPException(status_code=500, detail="Error listing videos")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Video Tagging API is running", "version": settings.API_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 