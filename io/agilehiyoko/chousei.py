#!/usr/bin/python

from bs4 import BeautifulSoup
from datetime import datetime as dt, timedelta as timedelta
import json
import requests


SITE_URL = 'https://chouseisan.com/schedule/newEvent/create'
WEEK_DAYS = ['月', '火', '水','木', '金', '土', '日']


def lambda_handler(event, context):
    # イベント開催日
    target_date_str = '2020-04-16 20:00:00'
    candidate_dates = manage_dates(target_date_str)

    session = requests.session()
    page_data = get_page_data(session, SITE_URL)
    soup = BeautifulSoup(page_data.text, 'html.parser')
    post_data = {
	'name': 'アジャイルひよこクラブ幹事会',
	'comment': 'アジャイルひよこクラブ幹事会日程を調整しましょう',
	'kouho': '\n'.join(candidate_dates)
    }
    event_page_url = create_new_event(session, post_data)
    print(event_page_url)


def get_page_data(session, url):
    response = session.get(url)
    response.encoding = response.apparent_encoding
    return response


def date_range(start_date, end_date):
    diff = (end_date - start_date).days + 1
    return (start_date + timedelta(i) for i in range(diff))


def date_back_range(base_date, period):
    yield from date_range(base_date - timedelta(period - 1), base_date)


def manage_dates(target_date_str):
    target_date = dt.strptime(target_date_str, '%Y-%m-%d %H:%M:%S')

    candidate_dates = []
    for day in date_back_range(target_date, 14):
        w = WEEK_DAYS[day.weekday()]
        if w in ['土', '日']:
            continue
        row = '{m}/{d}({w}) {H}:{M}〜'.format(
            m=dt.strftime(day, '%m'),
            d=dt.strftime(day, '%d'),
            w=w,
            H=dt.strftime(day, '%H'),
            M=dt.strftime(day, '%M'),
        )

        candidate_dates.append(row)
    return candidate_dates


def create_new_event(session, post_data):
    res = session.post(SITE_URL, post_data)
    result = BeautifulSoup(res.text, 'html.parser')
    result_url = result.find('input', {'class': 'new-event-url-input'})
    return result_url['value']


if __name__ == '__main__':
    lambda_handler(None, None)
