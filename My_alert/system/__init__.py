from flask import Flask
from flask import g
from flask import session
from flask import request
from flask import jsonify
from flask import make_response
from flask_cache import Cache
import pymongo
import os,sys


app = Flask(__name__)
app.secret_key = '2018052510144019940214'

cache = Cache(app, config={
                        'CACHE_TYPE': 'redis',              # Use Redis
                        'CACHE_REDIS_HOST': '127.0.0.1',    # Host, default 'localhost'
                        'CACHE_REDIS_PORT': 6379,           # Port, default 6379
                        'CACHE_REDIS_PASSWORD': '',         # Password
                        'CACHE_REDIS_DB': 0                 # DB, default 0
                    })

global_config = {
    'MESSAGE_MAX': 5,
    'ALERT_CRON': 10,
    'ALERT_DELAY': 10
}

wechat_config = {
    'CorpID': '',
    'AppSecret': {
        '1000002': '',
        '1000003': '',
        '1000004': '',
        '1000005': ''
    },
    'AgentID': {
        'Disaster': '1000005',
        'High': '1000004',
        'Average': '1000002',
        'Callback': '1000003'
    },
    'Callback': {
        'sToken': '',
        'sEncodingAESKey': ''
    }
}

Mongodb = pymongo.MongoClient('127.0.0.1', 27017).get_database('Malert')


from .action.wechat import alert
from .action.wechat import callback
from .tools import task

task.sched.start()

