from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    # Extract video ID from YouTube URL
    video_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return video_id.group(1) if video_id else None

def get_transcript(video_url, language='ru'):
    video_id = get_video_id(video_url)
    if not video_id:
        print("Invalid YouTube URL")
        return None

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {str(e)}")
        return None

def clean_transcript(transcript):
    # Combine all text entries and remove timestamps
    full_text = ' '.join(entry['text'] for entry in transcript)
    
    # Remove any remaining square brackets and their contents (often used for sound descriptions)
    full_text = re.sub(r'\[.*?\]', '', full_text)
    
    # Remove extra whitespace
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    
    return full_text

def main():
    video_url = input("Enter the YouTube video URL: ")
    transcript = get_transcript(video_url)
    
    if transcript:
        clean_text = clean_transcript(transcript)
        print("\nCleaned Transcript:")
        print(clean_text)
    else:
        print("Failed to retrieve transcript.")

if __name__ == "__main__":
    main()
