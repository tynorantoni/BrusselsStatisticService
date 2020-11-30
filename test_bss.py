import datetime
import psycopg2
import pytest
import requests
from requests import RequestException
import pingpong
from dbconnector import connect_to_db
from jsonmanipulation import list_of_all_counters, get_json_from_location, count_all_the_cyclists


class TestClass:

    # sets connection to DB
    @pytest.fixture()
    def setUp(self):
        connection = connect_to_db()
        yield connection
        connection.close()


    # test is service connected to DB
    def test_connect_to_db(self, setUp):
        cur = setUp.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        assert db_version is not None


    # creating a table
    def test_create_table(self, setUp):
        try:
            cur = setUp.cursor()

            cur.execute('''CREATE TABLE brussels_data_test_table
            (id SERIAL PRIMARY KEY NOT NULL,
            date_of_count DATE,
            street_name TEXT,
            day_cnt VarChar(10));'''
                        )

            setUp.commit()
            cur.execute('SELECT * FROM brussels_data_test_table;')

            assert cur.fetchone() == 'None'

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            cur.close()


    # insert prepared data to test table
    def test_insert_to_db(self, setUp):
        date = datetime.date(2019, 12, 24)
        try:
            cur = setUp.cursor()

            cur.execute('''INSERT INTO brussels_data_test_table 
            (date_of_count, street_name, day_cnt) VALUES 
            ({},{},{});'''.format(date, "'test_street'", 666)
                        )

            setUp.commit()

            cur.execute('SELECT day_cnt FROM brussels_data_test_table;')
            assert cur.fetchone() == 666

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            cur.close()


    # drop test table after tests
    def test_drop_table(self, setUp):
        try:
            cur = setUp.cursor()

            cur.execute('''DROP TABLE brussels_data_test_table;''')
            # setUp.commit()
            assert cur.statusmessage == 'DROP TABLE'
        except psycopg2.DatabaseError as error:
            print(error)


    # get list of all counters on brussels streets
    def test_list_of_all_counters(self):
        assert len(list_of_all_counters()) == 20


    # should receive json from location CB2105
    def test_get_json_from_location(self):
        start_date = datetime.date(2019, 12, 24)
        end_date = datetime.date(2019, 12, 25)
        device_id = 'CB2105'
        try:
            url = 'https://data.mobility.brussels/bike/api/counts/' \
                  '?request=history&featureID={}&startDate={}&endDate={}&outputFormat=json' \
                .format(device_id, start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"))

            request = requests.get(url)
            json = request.json()

            assert "'average_speed': 26" in str(json)

        except RequestException as error:
            print(error)


    # check counting function
    def test_count_all_the_cyclists(self):
        json = get_json_from_location('CB2105', datetime.date(2019, 12, 24), datetime.date(2019, 12, 25))

        assert count_all_the_cyclists(json) > 0

    # @pytest.fixture()
    # def setUpFlask(self):
    #     pingpong.app.testing = True
    #
    #     with pingpong.app.test_client() as client:
    #         with pingpong.app.app_context():
    #             pingpong.start()
    #         yield client
    #
    # def test_pong(self,setUpFlask):
    #     value = setUpFlask.get('/ping')
    #     assert '200' in str(value)


if __name__ == '__main__':
    pytest.main()
