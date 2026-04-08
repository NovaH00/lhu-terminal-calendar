from dataclasses import dataclass

class APIConfigs:
    # The URL to fetch calendar data
    LHU_API_URL: str = "https://tapi.lhu.edu.vn/calen/auth/XemLich_LichSinhVien"
    # Day range is how many days that has schedule to be shown
    DEFAULT_DAY_RANGE: int = 4

class CacheConfigs:
    # Time-to-live for the cache
    TTL_HOURS: int = 24
    # App name is used to create platfrom-specific cache location
    APP_NAME: str = "lhu-calendar"

