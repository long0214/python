# encodint: utf-8
import requests

'''
    This is a example coded by python
    level: ['Disaster', 'High', 'Average', 'Callback']
'''

url='http://115.159.29.45/wechat/alert.action'
url_callback='http://115.159.29.45/wechat/callback.action'

post_data = {
    'level': 'Average',
    'message': '233333333'
}

response = requests.post(url=url, data=json.dumps(post_data))
print(response.json())
