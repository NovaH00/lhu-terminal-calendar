from src.core.lhu_calen_api import LHUCalenAPI
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from src.utils.env import get_env

api = LHUCalenAPI(
    get_env("API_URL"),
    get_env("STUDENT_ID")
)

print(api.get_data(datetime(2025, 3, 2), 1))
