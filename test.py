from src.core.lhu_calen_api import LHUCalenAPI
from src.core.configurations import APIConfigs
from src.core.cache import CacheManager
from datetime import datetime, timezone
import requests
import json

# api = LHUCalenAPI(APIConfigs.LHU_API_URL, "124000095")
# print(api.get_data(4))
#
payload = {
    "StudentID": "124000095",
    "Ngay": datetime.now(timezone.utc),
    "PageIndex": 1,
    "PageSize": 30
}
res = requests.post(APIConfigs.LHU_API_URL, payload, timeout=10)

print(json.dumps(res.json(), ensure_ascii=False, indent=2))


