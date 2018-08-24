#!/bin/env  python

import requests
import time
from random import randint
import hmac, hashlib, base64
import json

#global config
Host='bj.file.myqcloud.com'
Appid = '1252875055'
Secret_id = ''
Secret_key = ''
Base_url='http://bj.file.myqcloud.com/files/v2/1252875055'


#encrypt
def encrypt(sign_name):
    return base64.b64encode(hmac.new(Secret_key, sign_name, digestmod=hashlib.sha1).digest() + sign_name)


def sign_name(bucket=None):
    if bucket == None:
        print 'bucket is None'
        return False
    now_time = int(time.time())
    expired = now_time + 60
    onceExpired = 0
    rdm = randint(1, 9999999999)
    fileid = ''
    multi_sign_name = 'a=' + Appid + '&b=' + bucket + '&k=' + Secret_id + '&e=' + str(expired) + '&t=' + str(now_time) + '&r=' + str(rdm) + '&f='
    once_sign_name = 'a=' + Appid + '&b=' + bucket + '&k=' + Secret_id + '&e=' + str(onceExpired) + '&t=' + str(now_time) + '&r=' + str(rdm) + '&f=' + fileid
    sn_dict = dict()
    sn_dict['multi'] = encrypt(multi_sign_name)
    sn_dict['once'] = encrypt(once_sign_name)
    return sn_dict


def mkdir(bucket=None, dirname=None):
    mkdir_url = '/'.join((Base_url, bucket, dirname)) + '/'
    #request header
    headers = {
        'Content-Type': 'application/json',
        'Authorization': sign_name(bucket=bucket)['multi']
    }
    data = {
        'op': 'create',
        'biz_attr': ''
    }
    post_data = json.dumps(data)
    http_session = requests.session()
    response = http_session.post(url=mkdir_url, headers=headers, data=post_data)
    return json.dumps(response.json(), indent=4)


def uploadfile(bucket=None, dirname=None, filename=None):
    upload_url = '/'.join((Base_url, bucket, dirname, filename))
    headers = {
        'Authorization': sign_name(bucket=bucket)['multi']
    }
    with open(filename, 'rb') as fd:
        filecontent = fd.read()
    http_body = dict()
    http_body = {
        'op': ('op', 'upload'),
        'filecontent': (filename, filecontent, 'application/octet-stream'),
        'sha1':('sha1', hashlib.sha1(filecontent).hexdigest()),
        'insertOnly': ('insertOnly', '0')
    }
    http_session = requests.session()
    response = http_session.post(url=upload_url, headers=headers, files=http_body)
    return json.dumps(response.json(), indent=4)


def main():
    #config
    bucket = 'mkeng'
    dirname = 'ab'
    filename='note'
    #print mkdir(bucket=bucket, dirname=dirname)
    print uploadfile(bucket=bucket, dirname=dirname, filename=filename)
    

if __name__ == '__main__':
    main()
