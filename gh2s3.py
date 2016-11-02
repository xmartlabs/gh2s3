#!/usr/bin/env python3

import boto3
import concurrent.futures
from datetime import datetime, timedelta
from gzip import GzipFile
from io import BytesIO
import os
import requests
from rx import Observable

THREADS = 30

S3 = boto3.resource('s3')

S3_BUCKET = S3.Bucket(os.environ['S3_BUCKET'])


def json_file_name_for_datetime(_datetime):
    return '{year}-{month:02}-{day:02}-{hour}.json'.format(year=_datetime.year, month=_datetime.month,
                                                           day=_datetime.day, hour=_datetime.hour)


def upload_hour_data_to_s3(_datetime, url):
    print("Requesting", url)
    response = requests.get(url)
    if response.status_code != 200:
        print(response)
    json_string = GzipFile(fileobj=BytesIO(response.content)).read()
    S3_BUCKET.put_object(Key=json_file_name_for_datetime(_datetime), Body=json_string)


with concurrent.futures.ProcessPoolExecutor(THREADS) as executor:
    # noinspection PyUnresolvedReferences
    Observable \
        .just(datetime(2016, 1, 1, hour=0)) \
        .repeat() \
        .scan(lambda last_datetime, _: last_datetime + timedelta(hours=1)) \
        .take_while(lambda _datetime: _datetime.month < 11) \
        .map(lambda _datetime: (_datetime, 'http://data.githubarchive.org/{}.gz'.format(json_file_name_for_datetime(
             _datetime)))) \
        .flat_map(lambda datetime_url_tuple: executor.submit(upload_hour_data_to_s3, *datetime_url_tuple)) \
        .subscribe()
