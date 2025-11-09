import os, json
from dotenv import load_dotenv
from openai import openai
from tools import get_weater, get_news, get_calendar_events

load_dotenv()
client = openai(api_key=os.getenv("OPENAI_API_KEY"))

# We define the available functions/tools declared in the tools.py file
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for given coordinates",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"},
                    "unit": {"type": "string", "enum": ["metric", "imperial"]},
                },
                "required": ["lat", "lon"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Fetch latest news headlines or by topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "country": {"type": "string"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_calendar_events",
            "description": "List your upcoming calendar events",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

# The prompt we've given to the system to take up a particular persona
system_prompt = """You are a helpful assistant that can decide whether the user
is asking about weather, news, or their calendar. 
Use the correct tool and answer naturally with the data returned.
"""

def agent_chat(user_input):
    pass

if __name__ == "__main__":
    print("🤖 Agentic Chatbot Ready! Type your questions.") # Default statement that prints when the user starts the program
    while True: # Till the user doesn't break away from the system
        user = input("\nYou: ") # Allowing user to input text
        if user.lower() in ["quit", "exit"]: break # User's program break/exit conditions
        answer = agent_chat(user) # Running our main function based on the user input and storing it in a variable
        print(f"Bot: {answer}") # Printing down the answer we found out in the answer variable