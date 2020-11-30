from configparser import ConfigParser
import psycopg2


# get credentials to connect
def config(filename='database.ini', section='postgresql'):
    try:
        parser = ConfigParser()
        parser.read('database.ini')

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db
    except FileNotFoundError as error:
        print(error)


# connect using data from config function
def connect_to_db():
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
