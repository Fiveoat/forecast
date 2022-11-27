from datetime import datetime, timedelta
from typing import Optional, Any
import pandas
import pytest

from utils import (
    get_datetime,
    get_is_daylight,
    get_height,
    get_data_key,
    convert_value,
    DataKeyNotFound,
)

UTC_NOW = datetime.utcnow()
FORECAST_DATE = datetime(year=2022, month=10, day=19).date()


@pytest.mark.parametrize(
    "sunrise_time, sunset_time, tide_time",
    [
        (UTC_NOW, UTC_NOW + timedelta(hours=2), UTC_NOW + timedelta(hours=1)),
        (UTC_NOW, UTC_NOW + timedelta(hours=10), UTC_NOW + timedelta(hours=5)),
    ],
)
def test_get_is_daylight_when_given_day_hours(
    sunrise_time: datetime, sunset_time: datetime, tide_time: datetime
) -> None:
    assert get_is_daylight(sunrise_time, sunset_time, tide_time) is True


@pytest.mark.parametrize(
    "sunrise_time, sunset_time, tide_time",
    [
        (UTC_NOW, UTC_NOW + timedelta(hours=1), UTC_NOW + timedelta(hours=2)),
        (UTC_NOW, UTC_NOW + timedelta(hours=1), UTC_NOW + timedelta(hours=5)),
    ],
)
def test_get_is_daylight_when_given_non_day_hours(
    sunrise_time: datetime, sunset_time: datetime, tide_time: datetime
) -> None:
    assert get_is_daylight(sunrise_time, sunset_time, tide_time) is False


@pytest.mark.parametrize(
    "time, date",
    [
        ("3:00 AM(Wed 19 October)", "Wednesday 19 October 2022"),
        ("Sunrise: 3:00AM", "Wednesday 19 October 2022"),
        ("Sunset: 3:00AM", "Wednesday 19 October 2022"),
        ("Moonrise: 3:00AM", "Wednesday 19 October 2022"),
        ("Moonset: 3:00AM", "Wednesday 19 October 2022"),
    ],
)
def test_get_datetime(time: str, date: Optional[str]) -> None:
    correct_datetime = datetime(year=2022, day=19, month=10, hour=3)
    derived_datetime = get_datetime(time, date)
    assert type(derived_datetime) == datetime
    assert derived_datetime == correct_datetime


@pytest.mark.parametrize(
    "height, expected_height",
    [
        ("1.05 ft (0.32 m)", 1.05),
        ("4.05 ft (1.23 m)", 4.05),
        ("1.19 ft (0.36 m)", 1.19),
    ],
)
def test_get_height(height: str, expected_height: float) -> None:
    derived_height = get_height(height)
    assert derived_height == expected_height
    assert type(derived_height) == float


@pytest.mark.parametrize(
    "element, expected_data_key, expected_data_type",
    [
        ("10:14 PM(Wed 19 October)", "tide_time", "datetime"),
        ("1.05 ft (0.32 m)", "feet_height", "str"),
        ("Sunrise: 7:19AM", "sunrise_time", "datetime"),
        ("Sunset: 6:31PM", "sunset_time", "datetime"),
        ("Moonrise: 1:21AM", "moonrise_time", "datetime"),
        ("Moonset: 3:49PM", "moonset_time", "datetime"),
    ],
)
def test_get_data_key(element: str, expected_data_key: str, expected_data_type: str) -> None:
    data_key, data_type = get_data_key(element)
    assert data_key == expected_data_key
    assert data_type == expected_data_type


@pytest.mark.parametrize(
    "element",
    [
        ("10:14 (Wed 19 October)",),
        ("1.05 (0.32 m)",),
        ("sunrise: 7:19",),
        ("sunset: 6:31",),
        ("moonrise: 1:21",),
        ("moonset: 3:49",),
        ("",),
    ],
)
def test_get_data_key_with_invalid_key(element: str) -> None:
    with pytest.raises(DataKeyNotFound):
        get_data_key(element)


@pytest.mark.parametrize(
    "value, data_type, data_key, forecast_date, converted_value",
    [
        ("High Tide", "str", "tide_type", FORECAST_DATE, "High Tide"),
        (
            "3:00 PM(Wed 19 October)",
            "datetime",
            "tide_time",
            FORECAST_DATE,
            datetime(year=2022, month=10, day=19, hour=15),
        ),
        ("4.05 ft (1.23 m)", "str", "feet_height", FORECAST_DATE, 4.05),
        ("Low Tide", "str", "tide_type", FORECAST_DATE, "Low Tide"),
        ("1.05 ft (0.32 m)", "str", "feet_height", FORECAST_DATE, 1.05),
        (
            "Sunrise: 7:00AM",
            "datetime",
            "sunrise_time",
            FORECAST_DATE,
            datetime(year=2022, month=10, day=19, hour=7),
        ),
        (
            "Sunset: 6:00PM",
            "datetime",
            "sunset_time",
            FORECAST_DATE,
            datetime(year=2022, month=10, day=19, hour=18),
        ),
        (
            "Moonrise: 1:00AM",
            "datetime",
            "moonrise_time",
            FORECAST_DATE,
            datetime(year=2022, month=10, day=19, hour=1),
        ),
        (
            "Moonset: 3:00PM",
            "datetime",
            "moonset_time",
            FORECAST_DATE,
            datetime(year=2022, month=10, day=19, hour=15),
        ),
    ],
)
def test_convert_value(
    value: str,
    data_type: str,
    data_key: str,
    forecast_date: datetime.date,
    converted_value: Any,
) -> None:
    assert convert_value(value, data_type, data_key, forecast_date) == converted_value
