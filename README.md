# Video Tagging API

A FastAPI backend for a stock video tagging system using MongoDB Atlas with GridFS for video storage, OpenAI Whisper API for transcription, and ChatGPT (gpt-4o-mini) for keyword extraction and title generation.

## Features

- 🎥 **Video Upload & Storage**: Store videos in MongoDB GridFS
- 🎤 **AI Transcription**: Extract transcripts using OpenAI Whisper
- 🏷️ **Smart Tagging**: Generate relevant tags using ChatGPT
- 📝 **Title Generation**: Create engaging titles from content
- 🔍 **Search & Filter**: Search videos by tags and transcript content
- 📺 **Video Streaming**: Stream videos by ID
- 📄 **Pagination**: List videos with pagination support

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB Atlas with GridFS
- **AI Services**: OpenAI Whisper & ChatGPT
- **Deployment**: Render
- **Video Processing**: FFmpeg

## API Endpoints

### Core Endpoints

| Method | Endpoint            | Description                       |
| ------ | ------------------- | --------------------------------- |
| `GET`  | `/`                 | Health check                      |
| `POST` | `/upload`           | Upload video with AI processing   |
| `GET`  | `/videos`           | List all videos (with pagination) |
| `GET`  | `/video/{video_id}` | Stream video by ID                |
| `GET`  | `/search`           | Search videos by query            |

### Query Parameters

- `page` (int): Page number for pagination (default: 1)
- `limit` (int): Items per page (default: 10, max: 50)
- `query` (str): Search query for tags and transcript

## Environment Variables

Create a `.env` file with the following variables:

```env
MONGODB_URI=your_mongodb_atlas_connection_string
OPENAI_API_KEY=your_openai_api_key
DATABASE_NAME=video_tagging
FRONTEND_URL=http://localhost:3000
```

## Local Development

### Prerequisites

- Python 3.9+
- FFmpeg installed
- MongoDB Atlas account
- OpenAI API key

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Video_tagging
   ```

2. **Create virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp env.example .env
   # Edit .env with your credentials
   ```

5. **Start the server**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - ReDoc Documentation: http://localhost:8000/redoc

## Deployment on Render

### Prerequisites

- Render account
- MongoDB Atlas cluster
- OpenAI API key

### Deployment Steps

1. **Connect your repository to Render**

   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure the service**

   - **Name**: `video-tagging-api`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set environment variables**

   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_NAME`: `video_tagging`
   - `FRONTEND_URL`: Your frontend URL (optional)

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your application

### Render Configuration

The `render.yaml` file is already configured for automatic deployment:

```yaml
services:
  - type: web
    name: video-tagging-api
    runtime: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: MONGODB_URI
        sync: false
      - key: OPENAI_API_KEY
        sync: false
      - key: DATABASE_NAME
        value: video_tagging
    healthCheckPath: /
    autoDeploy: true
```

## Testing with Postman

### Collection Setup

1. **Import the API**

   - Open Postman
   - Import the API from: `http://your-render-url/docs/openapi.json`

2. **Set up environment variables**
   - Create a new environment
   - Add variable: `base_url` = `https://your-render-url`

### Test Endpoints

#### 1. Health Check

```
GET {{base_url}}/
```

#### 2. Upload Video

```
POST {{base_url}}/upload
Content-Type: multipart/form-data

Body (form-data):
- file: [Select video file]
- title: [Optional title]
```

#### 3. List Videos

```
GET {{base_url}}/videos?page=1&limit=10
```

#### 4. Search Videos

```
GET {{base_url}}/search?query=keyword&page=1&limit=10
```

#### 5. Stream Video

```
GET {{base_url}}/video/{{video_id}}
```

### Example Response (Upload)

```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Building Lifelong Customer Trust",
  "filename": "video.mp4",
  "tags": ["customer", "trust", "experience", "service"],
  "transcript": "Hello everyone, today we're going to talk about...",
  "upload_date": "2024-01-15T10:30:00Z",
  "file_size": 1024000,
  "duration": 61.14,
  "download_url": "https://your-render-url/video/507f1f77bcf86cd799439011"
}
```

## API Response Format

### Success Response

```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation completed successfully"
}
```

### Error Response

```json
{
  "status": "error",
  "error": "Error description",
  "message": "Detailed error message"
}
```

## File Structure

```
Video_tagging/
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── models.py            # Pydantic models
├── database.py          # MongoDB connection
├── services.py          # AI processing services
├── requirements.txt     # Python dependencies
├── render.yaml          # Render deployment config
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**

   - Verify your MongoDB Atlas connection string
   - Ensure your IP is whitelisted in MongoDB Atlas

2. **OpenAI API Error**

   - Check your OpenAI API key
   - Verify you have sufficient credits

3. **FFmpeg Not Found**

   - Install FFmpeg: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Ubuntu)

4. **Render Deployment Issues**
   - Check build logs in Render dashboard
   - Verify environment variables are set correctly

### Logs

- **Local**: Check terminal output
- **Render**: View logs in Render dashboard

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the GitHub repository or contact the development team.
