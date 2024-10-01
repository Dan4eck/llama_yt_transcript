import json
import os
from openai import OpenAI
from yt_transcript import get_transcript, clean_transcript

# Initialize OpenAI client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def fetch_youtube_transcript(video_url: str) -> str:
    try:
        transcript = get_transcript(video_url)
        if transcript:
            return clean_transcript(transcript)
        return "Failed to retrieve transcript."
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

def process_transcript_with_llm(user_input: str):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "fetch_youtube_transcript",
                "description": "Fetch and clean the transcript of a YouTube video",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "video_url": {
                            "type": "string",
                            "description": "The URL of the YouTube video",
                        },
                    },
                    "required": ["video_url"],
                },
            },
        }
    ]

    messages = [
        {"role": "system", "content": "You are an AI assistant that can fetch and analyze YouTube video transcripts. Use the provided function to get transcripts when needed."},
        {"role": "user", "content": user_input}
    ]

    try:
        response = client.chat.completions.create(
            model="llama3.2:3b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message
        print(f"Debug - Assistant message: {assistant_message}")

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                if tool_call.function.name == "fetch_youtube_transcript":
                    function_args = json.loads(tool_call.function.arguments)
                    transcript = fetch_youtube_transcript(function_args["video_url"])
                    print(f"Debug - Fetched transcript: {transcript[:100]}...")  # Print first 100 chars
                    
                    # Add the transcript to the messages
                    messages.append({
                        "role": "function",
                        "name": tool_call.function.name,
                        "content": transcript,
                    })
                    
                    # Add a system message to instruct the LLM to analyze the transcript
                    messages.append({
                        "role": "system",
                        "content": "Analyze the provided transcript and give a summary of its content. If the user asked a specific question, answer it based on the transcript."
                    })
                    
                    # Make a second call to process the transcript
                    second_response = client.chat.completions.create(
                        model="llama3.2:3b",
                        messages=messages,
                    )
                    return second_response.choices[0].message.content
        else:
            return assistant_message.content

    except Exception as e:
        return f"Error processing with LLM: {str(e)}"

def main():
    user_input = input("Enter your question: ")
    
    result = process_transcript_with_llm(user_input)
    print("\nLLM Response:")
    print(result)

if __name__ == "__main__":
    main()