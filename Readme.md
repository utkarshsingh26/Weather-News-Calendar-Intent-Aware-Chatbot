Step 1:

Create a virtual environment using (why do we create them, find out later)

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