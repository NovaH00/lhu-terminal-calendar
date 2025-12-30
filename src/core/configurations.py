from dataclasses import dataclass
from typing import ClassVar, override, Any, Never


# Metaclass that prevent class-object from modifying static attributes
class _ImmutableAttribute(type):
    """
    Explaination:
        In Python, classes are objects (created using the `type` function (see signature)), 
        and we can hook to the class creation process using metaclass. In this case we use
        `_ImmutableAttribute` metaclass to prevent `BaseConfigs` from modifying static attributes.

        The reason why we do this on the `BaseConfigs`'s metaclass and not in it-self is 
        because if we were overriden the `__setattr__` IN the BaseConfigs, it would just 
        prevent the objects instantiation by `BaseConfigs` from modifying attributes, not
        the `BaseConfigs` class it-self.
    """
    @override
    def __setattr__(self, key: str, value: Any) -> Never:
        raise AttributeError("read-only")

# Base config class that prevent instantiation
class _BaseConfigs(metaclass=_ImmutableAttribute):
    # Prevent instantiation
    def __new__(cls, *args, **kwargs) -> Never:
        raise TypeError("Config is static-only")


class APIConfigs(_BaseConfigs):
    # The URL to fetch calendar data
    LHU_API_URL: ClassVar[str] = "https://tapi.lhu.edu.vn/calen/auth/XemLich_LichSinhVien"
    # Day range is how many days that has schedule to be shown
    DEFAULT_DAY_RANGE: ClassVar[int] = 4

class CacheConfigs(_BaseConfigs):
    # Time-to-live for the cache
    TTL_HOURS: ClassVar[int] = 24
    # App name is used to create platfrom-specific cache location
    APP_NAME: ClassVar[str] = "lhu-calendar"

