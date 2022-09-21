from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from main import get_daylight_low_tides, Forecast, Tide, get_daily_forecast, get_day_forecast_soups

HALF_MOON_DAYLIGHT_LOW_TIDES = [
    {"feet_height": 2.47, "tide_type": "Low Tide", "tide_time": datetime(2022, 9, 22, 15, 23)},
    {"feet_height": 2.11, "tide_type": "Low Tide", "tide_time": datetime(2022, 9, 23, 15, 58)},
    {"feet_height": 1.72, "tide_type": "Low Tide", "tide_time": datetime(2022, 9, 24, 16, 32)},
    {"feet_height": 1.31, "tide_type": "Low Tide", "tide_time": datetime(2022, 9, 25, 17, 7)},
    {"feet_height": 0.9, "tide_type": "Low Tide", "tide_time": datetime(2022, 9, 26, 17, 44)},
    {"feet_height": 0.53, "tide_type": "Low Tide", "tide_time": datetime(2022, 9, 27, 18, 24)},
    {"feet_height": 2.66, "tide_type": "Low Tide", "tide_time": datetime(2022, 9, 30, 7, 40)},
    {"feet_height": 3.12, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 1, 8, 34)},
    {"feet_height": 3.43, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 2, 9, 51)},
    {"feet_height": 3.45, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 3, 11, 25)},
    {"feet_height": 3.13, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 4, 12, 48)},
    {"feet_height": 2.62, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 5, 13, 54)},
    {"feet_height": 2.02, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 6, 14, 49)},
    {"feet_height": 1.42, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 7, 15, 38)},
    {"feet_height": 0.87, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 8, 16, 24)},
    {"feet_height": 0.44, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 9, 17, 7)},
    {"feet_height": 0.13, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 10, 17, 49)},
    {"feet_height": -0.03, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 11, 18, 31)},
    {"feet_height": 3.1, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 14, 7, 49)},
    {"feet_height": 3.44, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 15, 8, 48)},
    {"feet_height": 3.61, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 16, 10, 9)},
    {"feet_height": 3.53, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 17, 11, 35)},
    {"feet_height": 3.26, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 18, 12, 45)},
    {"feet_height": 2.87, "tide_type": "Low Tide", "tide_time": datetime(2022, 10, 19, 13, 38)},
]

SUNRISE = datetime.now()
SUNSET = datetime.now() + timedelta(hours=10)
DAY_TIDE_TIME = datetime.now() + timedelta(hours=5)
NIGHT_TIDE_TIME = datetime.now() + timedelta(hours=11)
LOW_TIDE_HEIGHT = 1.0
HIGH_TIDE_HEIGHT = 21.0

DAY_LOW_TIDE = Tide(feet_height=LOW_TIDE_HEIGHT, tide_type="Low Tide", tide_time=DAY_TIDE_TIME)
NIGHT_LOW_TIDE = Tide(feet_height=LOW_TIDE_HEIGHT, tide_type="Low Tide", tide_time=NIGHT_TIDE_TIME)
DAY_HIGH_TIDE = Tide(feet_height=HIGH_TIDE_HEIGHT, tide_type="High Tide", tide_time=DAY_TIDE_TIME)
NIGHT_HIGH_TIDE = Tide(feet_height=HIGH_TIDE_HEIGHT, tide_type="High Tide", tide_time=NIGHT_TIDE_TIME)
DAY_FORECAST = Forecast(
    date=SUNRISE.date(),
    sunrise_time=SUNRISE,
    sunset_time=SUNSET,
    tides=[DAY_HIGH_TIDE, DAY_LOW_TIDE, NIGHT_LOW_TIDE, NIGHT_HIGH_TIDE],
)


def test_get_daylight_low_tides() -> None:
    daylight_low_tides = get_daylight_low_tides(DAY_FORECAST)
    assert len(daylight_low_tides) == 1
    for tide in daylight_low_tides:
        assert tide.tide_time == DAY_TIDE_TIME
        assert tide.feet_height == LOW_TIDE_HEIGHT
        assert tide.tide_type == "Low Tide"


def test_get_day_forecast_soups() -> None:
    with open("half_moon.html", "r") as html:
        soup = BeautifulSoup(html, "html.parser")
    assert len(get_day_forecast_soups(soup)) == 28


def test_get_daily_forecast() -> None:
    with open("half_moon.html", "r") as html:
        soup = BeautifulSoup(html, "html.parser")
    for index, day_forecast_soup in enumerate(get_day_forecast_soups(soup)):
        daily_forecast = get_daily_forecast(day_forecast_soup)
        assert type(daily_forecast) == Forecast
        assert len(daily_forecast.tides) in [3, 4]
        daylight_low_tides = get_daylight_low_tides(daily_forecast)
        for day_light_low_tide in daylight_low_tides:
            assert day_light_low_tide.dict() in HALF_MOON_DAYLIGHT_LOW_TIDES
        assert len(daylight_low_tides) in [0, 1, 2]
