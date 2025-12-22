from datetime import datetime, timezone

def parse_string_datetime(s: str) -> datetime:
    """
    Convert a datetime string (ISO) into a timezone-aware UTC `datetime` object.

    Args:
        value (str):
            Datetime string (e.g. "2025-12-23T09:30:00").
    Returns:
        datetime:
            A timezone-aware `datetime` object with `tzinfo=timezone.utc`.
    Raises:
        ValueError:
            If the input string does not match the expected datetime format.
    """
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


