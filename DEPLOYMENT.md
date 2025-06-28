# Deployment Checklist

## Pre-Deployment Setup

### 1. MongoDB Atlas Setup

- [ ] Create MongoDB Atlas account
- [ ] Create a new cluster
- [ ] Create database user with read/write permissions
- [ ] Get connection string from Atlas dashboard
- [ ] Whitelist Render IP addresses (0.0.0.0/0 for testing)

### 2. OpenAI API Setup

- [ ] Create OpenAI account
- [ ] Generate API key from https://platform.openai.com/api-keys
- [ ] Ensure sufficient credits for API calls

### 3. Render Account Setup

- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Verify repository access

## Deployment Steps

### 1. Repository Preparation

- [ ] All files committed to GitHub
- [ ] `render.yaml` configured correctly
- [ ] `requirements.txt` updated with correct versions
- [ ] `.env.example` includes all required variables

### 2. Render Deployment

- [ ] Create new Web Service in Render
- [ ] Connect GitHub repository
- [ ] Configure service settings:
  - Name: `video-tagging-api`
  - Runtime: `Python`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. Environment Variables

- [ ] Set `MONGODB_URI` (your MongoDB Atlas connection string)
- [ ] Set `OPENAI_API_KEY` (your OpenAI API key)
- [ ] Set `DATABASE_NAME` (default: `video_tagging`)
- [ ] Set `FRONTEND_URL` (optional, for CORS)

### 4. Deploy and Test

- [ ] Deploy the service
- [ ] Check build logs for errors
- [ ] Test health check endpoint: `GET /`
- [ ] Test video upload endpoint: `POST /upload`
- [ ] Test video listing endpoint: `GET /videos`
- [ ] Test search endpoint: `GET /search?query=test`

## Post-Deployment

### 1. API Documentation

- [ ] Access Swagger UI: `https://your-render-url/docs`
- [ ] Access ReDoc: `https://your-render-url/redoc`
- [ ] Test all endpoints through the UI

### 2. Postman Setup

- [ ] Import OpenAPI spec: `https://your-render-url/docs/openapi.json`
- [ ] Create environment with `base_url` variable
- [ ] Test all endpoints with Postman

### 3. Monitoring

- [ ] Set up logging in Render dashboard
- [ ] Monitor API usage and performance
- [ ] Check MongoDB Atlas metrics
- [ ] Monitor OpenAI API usage

## Troubleshooting

### Common Issues

1. **Build Failures**

   - Check `requirements.txt` for correct versions
   - Verify Python runtime compatibility

2. **MongoDB Connection Issues**

   - Verify connection string format
   - Check IP whitelist in MongoDB Atlas
   - Ensure database user has correct permissions

3. **OpenAI API Errors**

   - Verify API key is correct
   - Check API usage limits and credits
   - Ensure API key has access to Whisper and ChatGPT

4. **File Upload Issues**
   - Check file size limits
   - Verify supported file formats
   - Check FFmpeg availability on Render

### Support Resources

- [Render Documentation](https://render.com/docs)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Security Considerations

### Environment Variables

- [ ] Never commit `.env` files to repository
- [ ] Use Render's secure environment variable storage
- [ ] Rotate API keys regularly

### API Security

- [ ] Consider adding authentication for production
- [ ] Implement rate limiting
- [ ] Add CORS configuration for frontend
- [ ] Monitor for abuse and unusual usage

### Data Security

- [ ] Ensure MongoDB Atlas security settings
- [ ] Consider encrypting sensitive data
- [ ] Implement proper backup strategies
