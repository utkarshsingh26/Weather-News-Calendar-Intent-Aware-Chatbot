import os, json
from dotenv import load_dotenv
from openai import OpenAI
from tools import get_weather, get_news, get_calendar_events

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
system_prompt = """
You are an AI assistant with access to three tools:
1. get_weather(lat, lon, unit) — to get real-time weather data.
2. get_news(query, country) — to get news headlines.
3. get_calendar_events() — to fetch upcoming calendar events.

When the user message contains anything related to weather, location, temperature, or forecast:
→ Call get_weather immediately, using provided coordinates (lat/lon) if available.

When the user asks about news, headlines, or updates:
→ Call get_news.

When the user mentions meetings, events, or schedule:
→ Call get_calendar_events.

If you have enough information, call the right tool directly.
If you are missing parameters (like lat/lon), ask *only* for that, not for confirmation.

Always return a concise, natural-language answer to the user after calling a tool.
"""

def agent_chat(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        tools=tools
    )

    # If the LLM decides to call a tool
    tool_call = response.choices[0].message.tool_calls


    if tool_call:
        tool = tool_call[0]
        tool_id = tool.id
        tool_name = tool_call[0].function.name
        args = json.loads(tool_call[0].function.arguments or "{}")
        print(f"\n🛠️ Tool chosen: {tool_name} | Args: {args}\n")

        # Execute the correct tool
        if tool_name == "get_weather":
            result = get_weather(**args)
        elif tool_name == "get_news":
            result = get_news(**args)
        elif tool_name == "get_calendar_events":
            result = get_calendar_events()
        else:
            result = {"error": "Unknown tool"}
        
        # Send tool result back with the final answer
        final = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
                {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": tool.id,
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": json.dumps(args)
                            }
                        }
                    ]
                },
                {"role": "tool",
                "tool_call_id": tool.id,
                "name": tool_name,
                "content": json.dumps(result)
                }
            ]
        )

        return final.choices[0].message.content
    
    # The answer returned when the model didn't choose to use a tool
    return response.choices[0].message.content

if __name__ == "__main__":
    print("🤖 Agentic Chatbot Ready! Type your questions.") # Default statement that prints when the user starts the program
    while True: # Till the user doesn't break away from the system
        user = input("\nYou: ") # Allowing user to input text
        if user.lower() in ["quit", "exit"]: break # User's program break/exit conditions
        answer = agent_chat(user) # Running our main function based on the user input and storing it in a variable
        print(f"Bot: {answer}") # Printing down the answer we found out in the answer variable