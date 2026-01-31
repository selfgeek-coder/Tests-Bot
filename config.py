from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Config_obj:
    bot_token = getenv("BOT_TOKEN")
    groq_api_key = getenv("GROQ_API_KEY")
    database_url = getenv("DATABASE_URL")