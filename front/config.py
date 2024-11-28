import os

from dotenv import load_dotenv

load_dotenv()

debug = True if os.getenv("debug") in ["True", "true"] else False
api_url = os.getenv("api_url")
