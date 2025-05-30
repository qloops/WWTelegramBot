from datetime import datetime, timedelta, timezone


def convert_to_timezone(dt: datetime, offset_delta: timedelta) -> datetime:
    """
    Converts a datetime object to a datetime with time zone.

    Args:
        dt: datetime object (can be naive or aware)
        offset_delta: timedelta object representing the offset from UTC

    Returns:
        datetime object with time zone set
    """
    tz = timezone(offset_delta)
    
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)

    return dt.astimezone(tz)