from pprint import pprint
import requests as req

from config import settings
from src.schemas.weather import WeatherList, WeatherMoment, WeatherNow


class ExternalApi():
    def get_curent_weather(self, city_name: str):
        base_url = "http://api.weatherapi.com/v1/forecast.json"
        params = {
            'q': f"{city_name}",
            "days": 1,
            # "hour": 25,
            'key': settings.weater_api_key
        }
        response = req.get(base_url, params=params).json()
        # return response
        return WeatherList(
            current=WeatherNow.model_validate(response["current"]),
            forecast=[
                WeatherMoment.model_validate(data)
                for day in response["forecast"]["forecastday"]
                for data in day["hour"]
                ]
        )


if __name__ == "__main__":
    apis = ExternalApi()
    weahter = apis.get_curent_weather("Малаховка")
    print(weahter.compact_weather())


