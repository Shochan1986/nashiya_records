import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
from urllib.request import Request, urlopen


def get_weather_from_location_today(original_location):
    location = re.findall('\d{3}-\d{4}', original_location)
    url = "https://weather.yahoo.co.jp/weather/search/?p=" + location[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find(class_="serch-table")
    location_url = content.find('a').get('href')
    r =  requests.get(location_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find(id='yjw_pinpoint_today').find_all('td')
    info = []

    for each in content[1:]:
        info.append(each.get_text().strip('\n'))

    time = info[:8]
    weather = info[9:17]
    temperature = info[18:26]
    weather_info = [(time[i], weather[i], temperature[i]) for i in range(8)]

    result = [('{0[0]}: {0[1]}, {0[2]}°C'.format(weather_info[i])) for i in range(8)]
    result = ('{}\nの今日の天気は\n'.format(original_location) + '\n'.join(result) + '\nです。\n引用：yahoo!天気\n' + str(location_url))
    return result


def get_weather_from_location_tomorrow(original_location):
    location = re.findall('\d{3}-\d{4}', original_location)
    url = "https://weather.yahoo.co.jp/weather/search/?p=" + location[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find(class_="serch-table")
    location_url = content.find('a').get('href')
    r =  requests.get(location_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find(id='yjw_pinpoint_tomorrow').find_all('td')
    info = []

    for each in content[1:]:
        info.append(each.get_text().strip('\n'))

    time = info[:8]
    weather = info[9:17]
    temperature = info[18:26]
    weather_info = [(time[i], weather[i], temperature[i]) for i in range(8)]

    result = [('{0[0]}: {0[1]}, {0[2]}°C'.format(weather_info[i])) for i in range(8)]
    result = ('{}\nの明日の天気は\n'.format(original_location) + '\n'.join(result) + '\nです。\n引用：yahoo!天気\n' + str(location_url))
    return result


def yahoo_news(URL):
    rest = requests.get(URL)
    soup = BeautifulSoup(rest.text, "html.parser")
    data_list = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
    result = [(f'{data.span.string} {data.attrs["href"]}') for data in data_list]
    news = '\n'.join(map(str, result))
    return news
