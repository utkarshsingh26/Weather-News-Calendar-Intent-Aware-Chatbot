import requests, os
from datetime import datetime, timedelta

# This helps us get the weather from Open-Meteo (no API key needed for this)
def get_weather(lat: float, lon: float, unit: str = "metric"):
    url = "https://api.open-meteo.com/v1/forecast" # the api url
    params = {
        "latitude" : lat,
        "longitude" : lon,
        "current_weather" : True,
        "temperature_unit" : "celsius" if unit == metric else "fahrenheit"
    } # the params we'll send with the request
    res = requests.get(url, params=params).json() # actually making the request
    current = res.get("current_weather", {}) # taking out the current_weather section from the API output, the {} helps us return an empty object safely without running afowl
    return {
        "temperature" : current.get("temperature")
        "windspeed" : current.get("windspeed")
        "time" : current.get("time")
    }

# This helps us get news, does require the API key stored in the .env file
def get_news(query: str = "", country: str = "us"):
    key = os.getenv("NEWS_API_KEY") # grabbing the API key from the .env file
    endpoint = "https://newsapi.org/v2/top-headlines" # the API endpoint we'll be hitting
    params = {"country" : country, "q" : query or None, "apiKey" : key}
    res = requests.get(enpoint, params=params).json() # actually making the api request
    articles = res.get("articles", [])[:5] # grabbing the first five articles from the "articles" section of the response
    return [
        {"title" : a["title"], 
        "source" : a["source"]["name"],
        "url" : a["url"]
        }
        for a in articles
    ]

# This helps us get today's events from our fake calendar, later we can replace this with the actual Google Calendar API 
def get_calendar_events():
    now = datetime.now()
    events = [
        {"title": "Team Meeting" : "time": (now + timedelta(hours=2)),isoformat()}, # fake calendar entry 1 that'll help us verify the AI can infer to hit this function when needed
        {"title": "Dinner with Mom", "time": (now + timedelta(hours=6)).isoformat()} # fake calendar entry 2 that'll help us verify the AI can infer to hit this function when needed
    ]
    return events