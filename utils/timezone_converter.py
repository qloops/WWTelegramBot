import logging
from datetime import (
    datetime, 
    timedelta, 
    timezone
)

from tzlocal import get_localzone

logger = logging.getLogger(__name__)


def convert_to_utc(dt: datetime) -> datetime:
    """
    Converts any datetime to UTC, assuming local time if naive.

    Args:
        dt: A datetime object (naive or timezone-aware).

    Returns:
        datetime: A timezone-aware datetime object in UTC.
    """
    if dt.tzinfo is None:
        local_tz = get_localzone()
        dt = dt.replace(tzinfo=local_tz)

    return dt.astimezone(timezone.utc)


def shift_to_timezone(dt: datetime, offset_delta: timedelta) -> datetime:
    """
    Shifts a datetime (naive or timezone-aware) to a target timezone by applying 
        the given UTC offset.

    Naive datetime objects are assumedto be in UTC and will be shifted 
        accordingly.

    Args:
        dt: A datetime object, either naive (no timezone) or timezone-aware 
            offset_delta (constans.timezones.TIMEZONE): A timedelta representing 
            the target timezone's offset from UTC.

    Returns:
        datetime: A timezone-aware datetime object shifted to the target 
            timezone offset.
    """
    target_tz = timezone(offset_delta)

    if dt.tzinfo is None:
        # TODO: In all cases MongoDB and Pyrogram return datetime objects 
        # without tz_info, this needs to be fixed.
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(target_tz)