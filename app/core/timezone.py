from datetime import datetime
from zoneinfo import ZoneInfo


INDIA_TIMEZONE = ZoneInfo("Asia/Kolkata")


def get_current_india_datetime() -> datetime:
    return datetime.now(INDIA_TIMEZONE)


def get_current_india_date():
    return get_current_india_datetime().date()