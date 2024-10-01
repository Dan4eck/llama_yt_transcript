import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(verbose=True)

# Set environment variables explicitly if they're not loaded
if not os.getenv("OPENAI_API_BASE"):
    os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "ollama"

# Print environment variables for debugging
print("API Base:", os.getenv("OPENAI_API_BASE"))
print("API Key:", os.getenv("OPENAI_API_KEY"))

# Initialize OpenAI client
client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_llm_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3.2:3b",  # Make sure this matches the model name in Ollama
            messages=[
                {"role": "system", "content": "You are a smart ai assistant which can use yt_transcript tool to get the transcript from a provided url and provide a short summary of the video."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("Welcome to the Llama 3.2 test script!")
    print("Type 'exit' to quit the program.")
    
    while True:
        user_input = input("\nEnter your prompt: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        response = get_llm_response(user_input)
        print("\nLLM Response:")
        print(response)

if __name__ == "__main__":
    main()
