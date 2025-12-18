import os
from datetime import date, timedelta
from pirate_weather import forecast
from pirate_weather.api import PirateWeather
from pirate_weather.types.languages import Languages
from pirate_weather.types.units import Units
from pirate_weather.types.weather import Weather


def get_weather(name="Uniontown PA", LATLONG=(39.90008, -79.71643)):
    msg = ""
    weekday = date.today()
    pirate_weather = PirateWeather(os.environ.get('PIRATE_WEATHER'))

    latitude = 42.3601
    longitude = -71.0589
    forecast = pirate_weather.get_forecast(
        latitude, longitude,
        extend=False,  # default `False`
        lang=Languages.ENGLISH,  # default `ENGLISH`
        values_units=Units.AUTO,  # default `auto`
        exclude=[Weather.MINUTELY, Weather.ALERTS],  # default `[]`,
        timezone='UTC'  # default None - will be set by Pirate Weather API automatically
    )
    print(forecast.daily)

    msg += f"{name}: {forecast.daily.summary} Cloud Cover {forecast.currently.cloud_cover}\n"
    msg += "```\n"

    for day in forecast.daily:
        day = dict(day=date.strftime(weekday, '%a'),
                   sum=day.summary,
                   tempMin=day.temperature_min,
                   tempMax=day.temperature_max,

                   )
        msg +='{day}: {tempMin}°F - {tempMax}°F {sum}\n'.format(**day)
        weekday += timedelta(days=1)
    msg += "```"

    return msg


if __name__ == '__main__':
    LATLONG = 39.90008, -79.71643
    print(get_weather("Uniontown", (39.90008, -79.71643)))
