#!../python-venv/bin/python3

import python_weather
import asyncio
import os
import time
from datetime import datetime
import pdb

DEBUG=True

heavy_snow_list = ['THUNDERY_SNOW_SHOWERS', 'HEAVY_SNOW_SHOWERS', 'HEAVY_SNOW']
light_snow_list = ['LIGHT_SNOW_SHOWERS', 'LIGHT_SNOW', 'LIGHT_SLEET', 'LIGHT_SLEET_SHOWERS']
heavy_rain_list = ['THUNDERY_HEAVY_RAIN', 'THUNDERY_SHOWERS', 'HEAVY_RAIN', 'HEAVY_SHOWERS']
light_rain_list = ['LIGHT_RAIN', 'LIGHT_SHOWERS']
heavy_clouds = ['VERY_CLOUDY', 'CLOUDY', 'FOG']
partial_clouds = ['PARTLY_CLOUDY']
clear = ['SUNNY']

severityList = ['Sunny', 'PartlyCloudy', 'Cloudy', 'LightRain', 'HeavyRain', 'LightSnow', 'HeavySnow']

async def getweather(lookahead_count=3, lookahead_interval=3) -> None:
    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        now = datetime.now()
        temps = []
        winds = []
        conditions = []

        # fetch a weather forecast from a city
        weather = await client.get('Reston')

        if DEBUG:
            # returns the current day's forecast temperature (int)
            print(weather.temperature)

        for daily in weather:
            if DEBUG:
                print(daily)

            # hourly forecasts
            for hourly in daily:
                if DEBUG:
                    print(f' --> {hourly!r}')

                if hourly.time.hour >= now.hour and \
                   hourly.time.hour < now.hour + lookahead_count * lookahead_interval and \
                   daily.date == datetime.now().date():
                    temps.append(hourly.temperature)
                    winds.append(hourly.wind_speed)
                    conditions.append(hourly.kind)

    return temps, winds, conditions

if __name__ == '__main__':
    # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    # for more details
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    while True:
        temps, winds, conditions = asyncio.run(getweather())

        worstCondition = 'Sunny'
        for cond in conditions:
            if cond.name in heavy_snow_list and severityList.index('HeavySnow') >= severityList.index(worstCondition):
                worstCondition = 'HeavySnow'
            elif cond.name in light_snow_list and severityList.index('LightSnow') >= severityList.index(worstCondition):
                worstCondition = 'LightSnow'
            elif cond.name in heavy_rain_list and severityList.index('HeavyRain') >= severityList.index(worstCondition):
                worstCondition = 'HeavyRain'
            elif cond.name in light_rain_list and severityList.index('LightRain') >= severityList.index(worstCondition):
                worstCondition = 'LightRain'
            elif cond.name in heavy_clouds and severityList.index('Cloudy') >= severityList.index(worstCondition):
                worstCondition = 'Cloudy'
            elif cond.name in partial_clouds and severityList.index('PartlyCloudy') >= severityList.index(worstCondition):
                worstCondition = 'PartlyCloudy'
            elif cond.name in clear and severityList.index('Sunny') >= severityList.index(worstCondition):
                worstCondition = 'Sunny'

        outtext='{t:{' + \
                ','.join([str(temps[0]), str(min(temps)), str(max(temps))]) + \
                '},' + \
                'w:{' + \
                ','.join([str(winds[0]), str(min(winds)), str(max(winds))]) + \
                '},' + \
                'p:{' + \
                ','.join([str(conditions[0]), str(worstCondition)]) + \
                '}}\n'

        with open('outfile', 'a') as outfile:
            outfile.write(outtext)

        # poll every 20 minutes
        time.sleep(1000*60*20)

