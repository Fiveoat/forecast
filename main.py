import datetime
from typing import List

import pandas
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from pydantic import BaseModel

from consts import TIDE_FORECAST_BASE_URL, LOCATIONS
from utils import get_data_key, get_is_daylight, convert_value


class Tide(BaseModel):
    feet_height: float
    tide_type: str
    tide_time: datetime.datetime


class Forecast(BaseModel):
    date: datetime.date
    sunrise_time: datetime.datetime
    sunset_time: datetime.datetime
    tides: List[Tide]


def get_daylight_low_tides(forecast: Forecast) -> List[Tide]:
    daylight_low_tides = []
    for tide in forecast.tides:
        if tide.tide_type == "Low Tide" and get_is_daylight(
            forecast.sunrise_time, forecast.sunset_time, tide.tide_time
        ):
            daylight_low_tides.append(tide)
    return daylight_low_tides


def get_tide_forecast_soup(location: str) -> BeautifulSoup:
    html = requests.get(f"{TIDE_FORECAST_BASE_URL}/locations/{location}/tides/latest").text
    return BeautifulSoup(html, "html.parser")


def get_daily_forecast(day_forecast_soup: BeautifulSoup) -> Forecast:
    forecast = {"tides": []}
    forecast_date = day_forecast_soup.find_all("h4", {"class": "tide-day__date"})[0].text.split(": ")[1]
    forecast["date"] = parser.parse(forecast_date)
    for row in day_forecast_soup.find_all("tr"):
        tide = {}
        for element in row.find_all("td"):
            value = element.text.strip()
            if value:
                data_key, data_type = get_data_key(value)
                converted_value = convert_value(value, data_type, data_key, forecast_date)
                if "sun" in data_key or "moon" in data_key:
                    forecast[data_key] = converted_value
                else:
                    tide[data_key] = converted_value
        if tide:
            forecast["tides"].append(tide)
    return Forecast(**forecast)


def get_day_forecast_soups(soup: BeautifulSoup) -> List[BeautifulSoup]:
    return soup.find_all("div", {"class": "tide-day"})


def main() -> None:
    data = []
    for location in LOCATIONS:
        for day_forecast_soup in get_day_forecast_soups(get_tide_forecast_soup(location)):
            forecast = get_daily_forecast(day_forecast_soup)
            for daylight_low_tide_forecast in get_daylight_low_tides(forecast):
                daylight_low_tide_forecast = daylight_low_tide_forecast.dict()
                daylight_low_tide_forecast["sunrise_time"] = forecast.sunrise_time
                daylight_low_tide_forecast["sunset_time"] = forecast.sunset_time
                daylight_low_tide_forecast["location"] = location.lower().replace("-", "_")
                data.append(daylight_low_tide_forecast)
    pandas.DataFrame(data).to_csv(f"low_daylight_forecast.csv", index=False)


if __name__ == "__main__":
    main()
