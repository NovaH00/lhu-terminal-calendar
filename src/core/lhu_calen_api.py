from datetime import datetime, timezone, timedelta

import requests
from requests import Response
from pydantic import BaseModel
from src.utils.datetime import parse_string_datetime
from src.utils.cache import CacheManager

class CalenItem(BaseModel):
    start_time: datetime 
    end_time: datetime
    room_name: str
    subject_name: str
    facility_name: str 

class FailedToFetch(Exception):
    pass

class LHUCalenAPI:
    def __init__(self, api_url: str, student_id: str, cache_ttl_hours: int = 24) -> None:
        self._api_url: str = api_url
        self._student_id: str = student_id
        self._cache_manager: CacheManager = CacheManager(ttl_hours=cache_ttl_hours)
    
    def get_data(self, dt: datetime | None = None, day_range: int = 7) -> list[CalenItem]:
        if dt is None:
            dt = datetime.now(timezone.utc)
        elif dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        # Periodically clean expired cache entries (about 10% of the time)
        import random
        if random.random() < 0.1:  # 10% chance to clean expired cache files
            self._cache_manager.clear_expired()

        # Check cache first
        cached_result = self._cache_manager.get(
            self._api_url,
            self._student_id,
            dt,
            day_range
        )

        if cached_result is not None:
            # Convert cached data back to CalenItem objects
            # Need to convert ISO format datetime strings back to datetime objects
            reconstructed_items = []
            for item_dict in cached_result:
                # Convert ISO format strings back to datetime objects
                item_dict['start_time'] = datetime.fromisoformat(item_dict['start_time'])
                item_dict['end_time'] = datetime.fromisoformat(item_dict['end_time'])
                reconstructed_items.append(CalenItem(**item_dict))
            return reconstructed_items

        # Prepare payload and make API request
        payload = {
            "StudentID": self._student_id,
            "Ngay": dt,
            "PageIndex": 1,
            "PageSize": 30
        }

        res: Response = requests.post(self._api_url, payload)
        if not res.ok:
            raise FailedToFetch(
                f"Status code: {res.status_code}, reason: {res.reason}"
            )

        raw_data = res.json()["data"][2]
        parsed_data = [
            CalenItem(
                start_time = parse_string_datetime(d["ThoiGianBD"]),
                end_time = parse_string_datetime(d["ThoiGianKT"]),
                room_name = d["TenPhong"],
                subject_name =  d["TenMonHoc"],
                facility_name =  d["TenCoSo"],
            )
            for d in raw_data
        ]
        end_date = dt + timedelta(days=day_range)
        filtered_data = [
            item
            for item in parsed_data
            if item.end_time <= end_date and item.start_time >= dt
        ]

        # Store the result in cache
        # Convert CalenItem objects to dictionaries for JSON serialization
        cacheable_data: list[dict[str, str]] = []
        for item in filtered_data:
            item_dict = item.model_dump()
            # Convert datetime objects to ISO format strings for JSON serialization
            item_dict['start_time'] = item.start_time.isoformat()
            item_dict['end_time'] = item.end_time.isoformat()
            cacheable_data.append(item_dict)

        self._cache_manager.set(
            self._api_url,
            self._student_id,
            dt,
            day_range,
            cacheable_data
        )

        return filtered_data
