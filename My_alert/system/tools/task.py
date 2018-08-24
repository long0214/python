import threading
from apscheduler.scheduler import  Scheduler
import time
from system import global_config
from system import Mongodb
from system import cache
from system.tools.SendMessage import send
from system.models import db
from system.models.alert_history import alert_history

''' 
    every 3 seconds task
'''

sched = Scheduler()

@sched.interval_schedule(seconds=global_config['ALERT_CRON'], max_instances=10)
def alert_task():
    for i in Mongodb.alertmessages.find():
        projectname, level, messages = i['projectname'], i['level'], i['messages']
        # flag有效
        if str(cache.get(projectname + ':' + level)) != 'None':
            continue
        # flag过期
        if len(messages) <= global_config['MESSAGE_MAX']:
           for message in messages:
                t = threading.Thread(target=send_one, args=(projectname, level, message,))
                t.start()
        else:
            t = threading.Thread(target=send_more, args=(projectname, level, messages,))
            t.start()
    return 0

def send_one(projectname, level, message):
    alertid = str(round(time.time() * 1000))
    print(alertid + ':=====Send_One Start=====')
    print(level)
    print(message)
    result = send(level, message)
    print(alertid + ':', end='\t')
    print(result)
    if 'errcode' in result:
        if result['errcode'] == 0:
            if mysql_save(alertid, message):
                Mongodb.alertmessages.update_one({'projectname': projectname, 'level': level}, {"$pull": {'messages': message}})
    print(alertid + ':=====Send_One End=====')

    
def send_more(projectname, level, messages):
    alertid = str(round(time.time() * 1000))
    print(alertid + ':=====Send_More Start=====')
    print(level)
    print(messages)
    a = "项目名称:" + projectname
    b = "当前存在大量告警,请及时查看！！！！！"
    c = "详情回调ID:" + alertid
    to_one = '\n'.join([a, b, c])
    result = send(level, to_one)
    print(alertid + ':', end='\t')
    print(result)
    if 'errcode' in result:
        if result['errcode'] == 0:
            for message in messages:
                if mysql_save(alertid, message):
                    Mongodb.alertmessages.update_one({'projectname': projectname, 'level': level}, {"$pull": {'messages': message}})
    print(alertid + ':=====Send_More End=====')
    

def mysql_save(alertid, message):
    try:
        save_info = alert_history(alert_id=alertid, alert_message=message)
        db.session.add(save_info)
        db.session.commit()
        print(alertid + ':MySQL save success')
        return True
    except Exception as e:
        print(e)
        print(alertid + ':MySQL save failed')
        print('message: ' + message)
        return False
