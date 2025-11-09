Step 1:

Create a virtual environment using

python -m venv venv

Step 2:

.\venv\Scripts\activate

Step 3:

Install the necessary required libraries

pip install openai requests python-dotenv

Step 4:

Create these files

#1 .env -> Stores the necessary API Keys and URLs
#2 main.py -> This holds the agnetic logic
#3 tools.py -> This holds the real-world API functions

You will want to ask questions like:

What's 2+2?
What's on my calendar today?
What's on the news today?
What's the weather in Tempe today?


With this we have basically created an Agentic AI tool - We ask it a question, it decides whether it needs to access the tools we've given it, if it decides it needs to use them cause it's knowledge bank isn't robust enough then it takes action. This would not have been possible with a regular LLM model.

