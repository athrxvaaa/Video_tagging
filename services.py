import openai
import os
import tempfile
import subprocess
import logging
from typing import List
from config import settings

logger = logging.getLogger(__name__)

class VideoProcessingService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
        else:
            self.client = openai.OpenAI(api_key=self.api_key)

    def extract_transcript(self, video_data: bytes) -> str:
        """Extract transcript from video using OpenAI Whisper API"""
        try:
            # Save video to a temp file
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_video:
                temp_video.write(video_data)
                temp_video_path = temp_video.name

            # Extract audio to a temp file (MP3)
            temp_audio_path = temp_video_path.replace('.mp4', '.mp3')
            subprocess.run([
                "ffmpeg", "-y", "-i", temp_video_path, "-vn", "-acodec", "libmp3lame", temp_audio_path
            ], check=True)

            # Send audio to OpenAI Whisper API using legacy API
            with open(temp_audio_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                transcript = response.text

            # Clean up temp files
            os.remove(temp_video_path)
            os.remove(temp_audio_path)

            logger.info(f"Extracted transcript: {len(transcript)} characters")
            return transcript
        except Exception as e:
            logger.error(f"Error extracting transcript: {e}")
            return ""

    def generate_title_from_transcript(self, transcript: str, filename: str) -> str:
        """Generate a short, keyword-based title using ChatGPT"""
        try:
            if not transcript.strip():
                # Fallback to filename if no transcript
                return filename.replace('.mp4', '').replace('.avi', '').replace('.mov', '').replace('_', ' ').replace('-', ' ')
            
            prompt = f"""
            Based on this video transcript, generate a short, engaging title (3-6 words) that captures the main topic or theme.
            The title should be keyword-rich and descriptive.
            
            Transcript: {transcript[:1000]}  # Limit to first 1000 chars for efficiency
            
            Requirements:
            - 3-6 words maximum
            - Include relevant keywords
            - Be descriptive and engaging
            - No quotes or special formatting
            - Focus on the main topic or action
            
            Title:"""
            
            # Use legacy API for chat completion
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise, keyword-rich titles for videos based on their content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.7
            )
            
            title = response.choices[0].message.content.strip()
            
            # Clean up the title
            title = title.replace('"', '').replace("'", '').strip()
            
            # If title is too long, truncate it
            if len(title) > 50:
                title = ' '.join(title.split()[:6])
            
            logger.info(f"Generated title: {title}")
            return title
            
        except Exception as e:
            logger.error(f"Error generating title: {e}")
            # Fallback to filename
            return filename.replace('.mp4', '').replace('.avi', '').replace('.mov', '').replace('_', ' ').replace('-', ' ')

    def extract_tags_with_chatgpt(self, transcript: str, filename: str) -> List[str]:
        """Extract tags using ChatGPT for better keyword extraction"""
        try:
            if not transcript.strip():
                # Fallback to basic filename extraction
                return self._extract_basic_tags(filename)
            
            prompt = f"""
            Based on this video transcript, extract 10-15 relevant keywords/tags that would help with video search and categorization.
            
            Transcript: {transcript[:1500]}  # Limit to first 1500 chars for efficiency
            
            Requirements:
            - Extract 10-15 relevant keywords
            - Include topic-specific terms
            - Include action words and concepts
            - Focus on searchable terms
            - Return only the keywords, separated by commas
            - No explanations, just keywords
            
            Keywords:"""
            
            # Use legacy API for chat completion
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts relevant keywords and tags from video content for search optimization."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            keywords_text = response.choices[0].message.content.strip()
            
            # Parse keywords from response
            keywords = [kw.strip().lower() for kw in keywords_text.split(',') if kw.strip()]
            
            # Add some basic tags from filename
            filename_tags = self._extract_basic_tags(filename)
            
            # Combine and deduplicate
            all_tags = list(set(keywords + filename_tags))
            
            # Limit to max tags
            final_tags = all_tags[:settings.MAX_TAGS]
            
            logger.info(f"Extracted {len(final_tags)} tags: {final_tags}")
            return final_tags
            
        except Exception as e:
            logger.error(f"Error extracting tags with ChatGPT: {e}")
            # Fallback to basic extraction
            return self._extract_basic_tags(filename)

    def _extract_basic_tags(self, filename: str) -> List[str]:
        """Basic tag extraction from filename as fallback"""
        try:
            tags = []
            
            # Extract words from filename
            filename_words = filename.lower().replace('.', ' ').replace('_', ' ').replace('-', ' ').split()
            for word in filename_words:
                if len(word) > 3 and word not in tags:
                    tags.append(word)
            
            # Add common video tags
            common_tags = ['video', 'content', 'media']
            for tag in common_tags:
                if tag not in tags:
                    tags.append(tag)
            
            return tags[:10]  # Limit basic tags
            
        except Exception as e:
            logger.error(f"Error in basic tag extraction: {e}")
            return ['video']

    def extract_tags(self, text: str, filename: str) -> List[str]:
        """Main tag extraction method - now uses ChatGPT"""
        return self.extract_tags_with_chatgpt(text, filename)

# Global service instance
video_service = VideoProcessingService() 