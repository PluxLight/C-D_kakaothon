import json
import os
import requests
import pandas as pd

appKey = "0186d4f3-9543-4f4c-a776-2b3f0368818f"

# 현재 날씨(분별)
url_minutely = "https://api2.sktelecom.com/weather/current/minutely"

# 체감온도(현재)
url_wind_chill = 'https://api2.sktelecom.com/weather/index/wct'

anu_lat = '36.541607'
anu_long = '128.796446'

headers = {'Content-Type': 'application/json; charset=utf-8',
           'appKey': appKey}


def minutely(weather):
    # print(weather)
    # 상대 습도
    humidity = weather['humidity']

    # 기압정보
    # 현지기압(Ps)
    pressure_surface = weather['pressure']['surface']
    # 해면기압(SLP)
    pressure_seaLevel = weather['pressure']['seaLevel']

    # 관측소
    # 관측소명
    station_name = weather['station']['name']
    # 관측소 지점번호(stnid)
    station_id = weather['station']['id']
    # 관측소 유형
    # - KMA: 기상청 관측소
    # - BTN: SKP 관측소
    station_type = weather['station']['type']
    # 위도
    station_latitude = weather['station']['latitude']
    # 경도
    station_longitude = weather['station']['longitude']

    # 기온 정보
    # 오늘의 최고기온
    temperature_tmax = weather['temperature']['tmax']
    # 1시간 현재기온
    temperature_tc = weather['temperature']['tc']
    # 오늘의 최저기온
    temperature_tmin = weather['temperature']['tmin']

    # 낙뢰유무(해당 격자 내)
    # - 0: 없음
    # - 1: 있음
    lightning = weather['lightning']

    # 강수량
    # 강수형태코드
    # - 0: 현상없음 → rain(sinceOntime) 사용
    # - 1: 비       → rain(sinceOntime) 사용
    # - 2: 비/눈 → precipitation(sinceOntime) 사용
    # - 3: 눈    → precipitation(sinceOntime) 사용
    precipitation_type = weather['precipitation']['type']
    # 1시간 누적 강수량
    # - if type=0/1/2 → 강우량 (mm)
    # - if type=3     → 적설량 (cm)
    precipitation_sinceOntime = weather['precipitation']['sinceOntime']

    # 바람정보
    # 풍향 (dgree)
    wind_wdir = weather['wind']['wdir']
    # 풍속 (m/s)
    wind_wspd = weather['wind']['wspd']

    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    sky_name = weather['sky']['name']
    # 하늘상태코드
    sky_code = weather['sky']['code']

    # 강우정보
    # 1시간 누적 강우량
    rain_sinceOntime = weather['rain']['sinceOntime']
    # 일 누적 강우량
    rain_sinceMidnight = weather['rain']['sinceMidnight']
    # 10분 이동누적 강우량
    rain_last10min = weather['rain']['last10min']
    # 15분 이동누적 강우량
    rain_last15min = weather['rain']['last15min']
    # 30분 이동누적 강우량
    rain_last30min = weather['rain']['last30min']
    # 1시간 이동누적 강우량
    rain_last1hour = weather['rain']['last1hour']
    # 6시간 이동누적 강우량
    rain_last6hour = weather['rain']['last6hour']
    # 12시간 이동누적 강우량
    rain_last12hour = weather['rain']['last12hour']
    # 24시간 이동누적 강우량
    rain_last24hour = weather['rain']['last24hour']

    time = weather['timeObservation']

    str = '현재 온도 : ' + temperature_tc + '\n최고 온도 : ' + temperature_tmax + ', 최저 온도 : ' \
          + temperature_tmin + '\n하늘 상태 : ' + sky_name + '\n습도 : ' + humidity + ', 바람 : ' + wind_wspd \
          + '\n강수량 : ' + rain_sinceMidnight + '\n기준 시간 : ' + time
    return str


def wind_chill_parser(weather):
    #print(weather, '\n')

    now_wind_chill = weather['current']['index']  # 현재 체감 온도
    time = weather['current']['timeRelease']

    str = '현재 체감 온도 : ' + now_wind_chill + '\n기준 시간 : ' + time
    return str


def requestCurrentWeather(city, county, village):
    params = {"version": "1",
              "city": city,
              "county": county,
              "village": village}
    response = requests.get(url_minutely, params=params, headers=headers)

    if response.status_code == 200:
        response_body = response.json()

        weather_data = response_body['weather']['minutely'][0]
        return minutely(weather_data)


def windchill(lat, long):
    params = {"version": "1",
              "lat": lat,
              "lon": long}
    response = requests.get(url_wind_chill, params=params, headers=headers)

    if response.status_code == 200:
        response_body = response.json()
        wind_chill_data = response_body['weather']['wIndex']['wctIndex'][0]
        return wind_chill_parser(wind_chill_data)


def main_action():
    return (requestCurrentWeather('경북', '안동시', '송천동'))