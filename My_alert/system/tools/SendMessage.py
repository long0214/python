# encoding: utf-8
from system import cache
from system import wechat_config
import requests
import json

CorpID = 'ww247a4e381841cf88'

''' agentid: Secret '''
AppSecret = {
    '1000002': 'ivHV2D6F_npudDchixJ6tlOMnyHJHbmPwI5HYAX4qP8'
}
AgentID = {
    'Disaster': '',
    'High': '',
    'Average': '1000002'
}

def get_accessToken(agentid):
    key = "wechat:access_token:" + agentid
    # 缓存命中, 返回结果
    if str(cache.get(key)) != 'None':
        return {'success': True, 'result': cache.get(key)}
    # 缓存失效, 重新请求
    else:
        # 获取新AccessToken
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        get_params = {
            'corpid': wechat_config['CorpID'],
            'corpsecret': wechat_config['AppSecret'][agentid]
        }
        response = requests.get(url=url, params=get_params)
        # http 请求成功, 判断返回结果
        if response.status_code == 200:
            result = response.json()
            # 结果正常, access_token存入缓存并返回
            if result['errcode'] == 0:
                try:
                    cache.set("wechat:access_token:" + agentid, result['access_token'], 7100)
                    print('获取wechat token成功')
                    return {'success': True, 'result': cache.get(key)}
                except Exception as e:
                    print(e)
                    return {'success': False, 'result': 'Set cache faild'}
            # token获取失败, 返回报错信息
            else:
                print("Get token faild: " + result['errmsg'])
                return {'success': False, 'result': result['errmsg']}
        # http 请求失败, 返回status_code
        else:
            print("http requests faild: " + response.status_code) 
            return {'success': False, 'result': response.status_code}
        
    
def send(level, message, touser='@all'):
    # 根据报警级别, 获取agentid
    if level in wechat_config['AgentID']:
        agentid = wechat_config['AgentID'][level]
        # 获取access_token
        getToken = get_accessToken(agentid)
        if getToken['success'] == True:
            access_token = getToken['result']
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
            post_params = {
                "access_token": access_token
            }
            post_data = {
                "touser": touser,
                "msgtype": "text",
                "agentid": agentid,
                "text": {
                    "content": message
               },
               "safe": 0
            }
            response = requests.post(url=url, params=post_params, data=json.dumps(post_data))
            return response.json()
        else:
            return getToken
    else:
        return {'success': False, 'result': 'No such alert level'}
 
