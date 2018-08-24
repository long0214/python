from system import cache
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def bus_token():
    key = 'bus:access_token'
    if str(cache.get(key)) != 'None':
        print("缓存命中总线token")
        return cache.get('bus:access_token')
    url = 'https://turing.bus.cyou-inc.com/engine/auth/token.action'
    token_data = {
        "app_id": "2018012610183708990",
        "app_secret": "0344dafaf5f04916a59f372275b787fd"
    }

    ret = requests.post(url=url, data=json.dumps(token_data), verify=False)
    print("总线token http返回码:" + str(ret.status_code))
    if ret.status_code == 200:
        bus_token = ret.json()['access_token']
        expires_in = ret.json()['expires_in']
        cache.set('bus:access_token', bus_token, expires_in)
        print("总线token:" + bus_token)
        return bus_token
    else:
        print('Get Bus Token Failed')
        return False

def project():
    key = 'projectlist'
    if str(cache.get(key)) != 'None':
        print("获取应用产品列表命中缓存")
        return cache.get('projectlist')
    access_token = bus_token()
    url = 'https://turing.bus.cyou-inc.com/engine/service/jsonrpc.action?access_token=' + access_token
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "54",
        "params": {
            'all': 'true'
        }
    }
    ret = requests.post(url=url, data=json.dumps(data), verify=False)
    print("获取应用产品列表 http返回码:" + str(ret.status_code))
    if ret.status_code == 200:
        if ret.json()['id'] != None:
            allproject = [ i['productName'] for i in json.loads(ret.json()['result']) ]
            # 设置应用产品列表缓存半小时
            expires_in = 1800 
            cache.set('projectlist', allproject, expires_in)
            return allproject
        else:
            print("总线访问正常获取失败")
            print(ret.json())
    else:
        print("获取应用产品列表失败")
        return False

#ProjectList = project()

if __name__ == '__main__':
    project()
