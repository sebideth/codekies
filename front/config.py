import os

from dotenv import load_dotenv

load_dotenv()

debug = True if os.getenv("debug") in ["True", "true"] else False
api_url = os.getenv("api_url")
app_path = os.getenv("app_path")
statics_files_path = os.path.join(os.getenv("app_path"), os.getenv("statics_files"))
