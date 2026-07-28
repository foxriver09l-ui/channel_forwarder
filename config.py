import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])