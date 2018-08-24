from system import app
from system import jsonify
from system import request
from system import cache
from system import global_config
from system import Mongodb
from system.tools import SendMessage
from system.tools.Project import project
import json
import re

# Create your views here.
'''
    message
    告警级别:Alert Level
    告警主机:{HOST.NAME}
    告警IP:{HOST.IP}
    告警信息:{TRIGGER.NAME}
    告警时间:{EVENT.DATE}  {EVENT.TIME}

    alert flag: "projectname:alert"  string
'''
@app.route('/wechat/alert.action', methods=['GET', 'POST'])
def alert():
    if request.method == 'POST':
        post_data = json.loads(request.get_data().decode("utf-8"))
        # 检验参数
        if 'level' in post_data and 'message' in post_data:
            ProjectList = project()
            ProjectList.remove('*') # 应用产品列表里有个 *, Md哪个傻逼添加的
            level, message = post_data['level'], post_data['message']

            # 匹配 re_text:"告警主机"
            re_text = b'\xe5\x91\x8a\xe8\xad\xa6\xe4\xb8\xbb\xe6\x9c\xba'
            projectname = ''
            for i in message.split('\n'):
                if re.match(re_text, i.encode()):
                    # HOST.NAME 匹配项目名称
                    projectname = list(filter(lambda x: str(re.match(b'.*' + x.encode(), i.encode())) != 'None', ProjectList))
                    if len(projectname):
                        projectname = projectname[0]
                        print("项目名称匹配成功:" + projectname)
                        # 存入mongo
                        if Mongodb.alertmessages.count({'projectname': projectname, 'level': level}) == 1:
                            Mongodb.alertmessages.update_one({'projectname': projectname, 'level': level}, {"$push": {'messages': message}})
                            print("====追加报警信息成功====\n" + message)
                        else:
                            data = {
                                'projectname': projectname,
                                'level': level,
                                'messages': [message]
                            }
                            Mongodb.alertmessages.insert_one(data)
                            print("====添加项目告警信息成功====\n" + message)
                        # 设置告警flag
                        cache.set(projectname + ':' + level, 'no', global_config['ALERT_DELAY'])
                        return jsonify({'success': True, 'message': ''})
                    else:
                        return jsonify({'success': False, 'message': 'Match project name failed'})
            return jsonify({'success': False, 'message': 'Post message error'})
        return jsonify({'success': False, 'message': 'Params error'})
    return jsonify({'success': False, 'message': 'Method error'})

