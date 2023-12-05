import os

from dotenv import load_dotenv, find_dotenv

class Settings:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.openai_api_key = os.getenv("OPENAI_API_KEY")