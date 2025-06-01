import logging
from datetime import datetime, timedelta, timezone

from tzlocal import get_localzone

logger = logging.getLogger(__name__)


def convert_to_utc(dt: datetime) -> datetime:
    """
    Converts any datetime to UTC, assuming local time if naive.

    Args:
        dt: A datetime object (naive or timezone-aware).

    Returns:
        A timezone-aware datetime object in UTC.
    """
    if dt.tzinfo is None:
        local_tz = get_localzone()
        dt = dt.replace(tzinfo=local_tz)

    return dt.astimezone(timezone.utc)


def convert_to_timezone(dt: datetime, offset_delta: timedelta) -> datetime:
    """
    Converts any datetime (naive or timezone-aware) to a new timezone, 
    applying the correct time shift.

    Naive datetime objects are assumed to be in UTC and will be shifted accordingly.

    Args:
        dt: A datetime object (naive or aware).
        offset_delta: A timedelta representing the target timezone's offset from UTC.

    Returns:
        A timezone-aware datetime object with the time shifted to the target timezone.
    """
    target_tz = timezone(offset_delta)

    if dt.tzinfo is None:
        # TODO: In all cases MongoDB and Pyrogram return objects without tz_info, this needs to be fixed.
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(target_tz)