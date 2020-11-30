from flask import Flask
from flask_apscheduler import APScheduler
from flask_restful import Api
from pingpong import PingPong
import datetime

from jsonmanipulation import insert_all_data

#sets scheduled job for function
class Config(object):
    JOBS = [
        {
            'id': 'crawl_brussels_data',
            'func': 'app:get_json_from_api',
            'trigger': 'interval',
            'seconds': 86400
        }
    ]

    SCHEDULER_API_ENABLED = True


def get_json_from_api():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    insert_all_data(yesterday,yesterday)




#start flask app
app = Flask(__name__)
app.config.from_object(Config())
api = Api(app)

#add 'ping' routing
api.add_resource(PingPong, '/ping')

#enable schedule trigerring
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()



if __name__ == '__main__':
    app.run(host='0.0.0.0')

