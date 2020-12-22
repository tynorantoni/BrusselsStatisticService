import datetime

import psycopg2
import requests
from requests import RequestException

from dbconnector import connect_to_db
from dbmanipulation import insert_to_db

#returns list of all counters in brussels with ID
def list_of_all_counters():
    try:
        device_url = 'https://data.mobility.brussels/bike/api/counts/?request=devices'
        device_req = requests.get(device_url)
        json = device_req.json()
        count = 0
        device_dict = {}
        for j in json['features']:
            road_name = json['features'][count]['properties']['road_en'].replace("'", " ") #street name
            device_id = json['features'][count]['properties']['device_name'] #id
            device_dict[road_name] = device_id
            count += 1
        return device_dict
    except RequestException as error:
        print(error)

#returns json from brussels api, with data about cyclists
def get_json_from_location(device_id, start_date, end_date):
    try:
        url = 'https://data.mobility.brussels/bike/api/counts/' \
              '?request=history&featureID={}&startDate={}&endDate={}&outputFormat=json' \
            .format(device_id, start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"))

        request = requests.get(url)
        json = request.json()
        return json
    except RequestException as error:
        print(error)

#counting number of cyclists from brussels street
def count_all_the_cyclists(json):
    try:
        total_value = 0
        for j in json['data']:
            total_value += j['count']

        return total_value
    except Exception as error:
        print(error)


#function combining returned data, inserting to DB
def insert_all_data(start_date, end_date):
    conn = connect_to_db()
    delta = datetime.timedelta(days=1)
    devices = list_of_all_counters()
    while start_date <= end_date:
        for device in devices:
            json = get_json_from_location(devices[device], start_date, start_date)
            no_of_cyclists = count_all_the_cyclists(json)
            insert_to_db(conn, start_date, device, no_of_cyclists)
        start_date += delta
    conn.close()


#funtion used to fill up DB with data from 2018 till now
def insert_all_data_temp():
    print('lets go!')
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        start_date = datetime.date(2018, 12, 5)
        end_date = datetime.date(2020, 11, 30)
        delta = datetime.timedelta(days=1)
        devices = list_of_all_counters()
        while start_date <= end_date:
            print('still working... ', start_date)
            for device in devices:
                json = get_json_from_location(devices[device], start_date, start_date)
                no_of_cyclists = count_all_the_cyclists(json)

                cur.execute('''INSERT INTO brussels_data 
                        (date_of_count, street_name, day_cnt) VALUES 
                        ('{}','{}',{});'''.format(start_date, device, no_of_cyclists)
                            )
                conn.commit()
            start_date += delta
        print('success?')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
