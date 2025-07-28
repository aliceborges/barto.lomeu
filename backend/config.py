import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_NAME = os.getenv("DB_NAME", "urls.db")
    BASE_URL = os.getenv("BASE_URL", "http://localhost/")
