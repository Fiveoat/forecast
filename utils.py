import datetime
from typing import Tuple, Union, Any

from dateutil import parser


class DataKeyNotFound(ValueError):
    def __init__(self, element):
        super().__init__(f"Element {element} not found as an option.")


def get_datetime(time: str, date: Union[str, datetime.date]) -> datetime.datetime:
    if "(" in time:
        time, date = time.split("(")
        return parser.parse(f"{date.replace(')', '')} {time}")
    time = time.split(":", 1)[1].strip()
    return parser.parse(f"{date} {time}")


def convert_value(value: str, data_type: str, data_key: str, forecast_date: datetime.date) -> Any:
    if "sun" in data_key or data_type == "datetime":
        return get_datetime(value, forecast_date)
    if data_key == "feet_height":
        return get_height(value)
    return value


def get_is_daylight(
    sunrise_time: datetime.datetime,
    sunset_time: datetime.datetime,
    tide_time: datetime.datetime,
) -> bool:
    return sunrise_time < tide_time < sunset_time


def get_height(height: str) -> float:
    return float(height.split(" ft")[0])


def get_data_key(element: str) -> Tuple[str, str]:
    if "Tide" in element:
        return "tide_type", "str"
    if "Sunrise" in element:
        return "sunrise_time", "datetime"
    if "Sunset" in element:
        return "sunset_time", "datetime"
    if "Moonrise" in element:
        return "moonrise_time", "datetime"
    if "Moonset" in element:
        return "moonset_time", "datetime"
    if "AM" in element or "PM" in element:
        return "tide_time", "datetime"
    if "ft" in element:
        return "feet_height", "str"
    raise DataKeyNotFound(element)
