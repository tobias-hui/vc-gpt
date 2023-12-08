import os

from dotenv import load_dotenv, find_dotenv

class Settings:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.pdf_api_key = os.getenv("PDF_API_KEY")
        self.pdf_secret_key = os.getenv("PDF_API_SECRET")