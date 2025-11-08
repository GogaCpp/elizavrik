from pydantic import BaseModel, ConfigDict, Field


class WeatherNow(BaseModel):
    model_config = ConfigDict(extra='ignore')

    last_updated_epoch: int = Field(..., description="Локальное время и дата")

    temp_c: float = Field(..., description="Температура в градусах Цельсия", ge=-100, le=100)
    feelslike_c: float = Field(..., description="Ощущаемая температура в градусах Цельсия", ge=-100, le=100)

    cloud: int = Field(..., description="Облачность в процентах", ge=0, le=100)

    wind_kph: float = Field(..., description="Скорость ветра в километрах в час", ge=0)
    wind_dir: str = Field(..., description="Направление ветра")

    pressure_mb: float = Field(..., description="Атмосферное давление в миллибарах", ge=800, le=1100)


class WeatherMoment(BaseModel):
    model_config = ConfigDict(extra='ignore')

    time_epoch: int = Field(..., description="Локальное время и дата")

    temp_c: float = Field(..., description="Температура в градусах Цельсия", ge=-100, le=100)
    feelslike_c: float = Field(..., description="Ощущаемая температура в градусах Цельсия", ge=-100, le=100)

    cloud: int = Field(..., description="Облачность в процентах", ge=0, le=100)

    wind_kph: float = Field(..., description="Скорость ветра в километрах в час", ge=0)
    wind_dir: str = Field(..., description="Направление ветра")

    pressure_mb: float = Field(..., description="Атмосферное давление в миллибарах", ge=800, le=1100)


class WeatherList(BaseModel):
    current: WeatherNow
    forecast: list[WeatherMoment]

    def compact_weather(self) -> dict:
        current = self.current
        forecast = self.forecast

        times = [str(m.time_epoch) for m in forecast]
        temps = [str(m.temp_c) for m in forecast]
        winds = [str(m.wind_kph) for m in forecast]
        clouds = [str(m.cloud) for m in forecast]
        pressure = [str(m.pressure_mb) for m in forecast]

        return {
            "time": f"{current.last_updated_epoch}{"->".join(times)}",
            "temp": f"{current.temp_c}{"->".join(temps)}",
            "wind": f"{current.wind_dir}{"->".join(winds)}",
            "cloud": f"{current.cloud}{"->".join(clouds)}",
            "pressure": f"{current.pressure_mb}{"->".join(pressure)}"
        }