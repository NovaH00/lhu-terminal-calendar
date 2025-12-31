from datetime import datetime, timezone, timedelta
import random

import requests
from requests import Response
from pydantic import BaseModel
from src.core.configurations import CacheConfigs
from src.utils.datetime import parse_string_datetime
from src.core.cache import CacheManager

class CalenItem(BaseModel):
    start_time: datetime 
    end_time: datetime
    room_name: str
    subject_name: str
    facility_name: str 

class ConnectionError(Exception):
    pass

class TimeoutError(Exception):
    pass

class LHUCalenAPI:
    def __init__(self, api_url: str, student_id: str, cache_manager: CacheManager) -> None:
        self._api_url: str = api_url
        self._student_id: str = student_id
        self._cache_manager: CacheManager = cache_manager 
    
    def get_data(self, day_range: int, dt: datetime | None = None) -> list[CalenItem]:
        """Fetch data from the API, use current time if `dt` is not provided
        
        Raises:
            `ConnectionError` : When having network errors
            `TimeoutError` : When the request have not responsed within 10s 
        """

        if dt is None:
            dt = datetime.now(timezone.utc)
        elif dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        # Periodically clean expired cache entries (about 10% of the time)
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
            return [
                CalenItem.model_validate_json(item_dict)
                for item_dict in cached_result
            ]

        # Prepare payload and make API request
        payload = {
            "StudentID": self._student_id,
            "Ngay": dt,
            "PageIndex": 1,
            "PageSize": 30
        }

        try:
            res: Response = requests.post(self._api_url, payload, timeout=10)
            res.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise ConnectionError()
        except requests.exceptions.Timeout:
            raise TimeoutError()
         
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
        cacheable_data = [
            item.model_dump_json()
            for item in filtered_data
        ]
        
        self._cache_manager.set(
            self._api_url,
            self._student_id,
            dt,
            day_range,
            cacheable_data
        )

        return filtered_data
