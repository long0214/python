# encoding: utf-8
import time
import uuid
import json
import requests
import sxtwl
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.request import RpcRequest


def send_sms(name):
    REGION = "cn-hangzhou"
    PRODUCT_NAME = "Dysmsapi"
    DOMAIN = "dysmsapi.aliyuncs.com"

    # need modify
    ACCESS_KEY_ID='YourKey'
    ACCESS_KEY_SECRET='YourSecret'

    TemplateParam = {"name": name}
    rpc_request = RpcRequest('Dysmsapi', '2017-05-25', 'SendSms')
    rpc_request.add_query_param('TemplateCode', 'SMS_77130046')
    rpc_request.add_query_param('TemplateParam', json.dumps(TemplateParam))
    rpc_request.add_query_param('OutId', uuid.uuid1())
    rpc_request.add_query_param('SignName', 'MKeng提醒')
    rpc_request.add_query_param('PhoneNumbers', '18829028766')

    region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)
    acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
    response = acs_client.do_action_with_exception(rpc_request)
    return response


def check_birth(item):
    date = time.localtime()
    name, month, day, flag = item.strip('\n').split()
    if int(flag) == 1:
        if int(month) == date.tm_mon and int(day) == date.tm_mday:
            return True
    else:
        lunar = sxtwl.Lunar()
        day = lunar.getDayByLunar(date.tm_year, int(month), int(day))
        if day.m == date.tm_mon and day.d == date.tm_mday:
            return True
    return False


def main():
    birthdays = [
        "# 1:公历  0:农历",
        "MQL 2   14  1",
        "LMX 2   14  1",
        "RY  11  11  0",
        "TYB 10  28  1",
        "JY  1   5   0",
        "LY  12  1   0",
        "hh  7   14  0"
    ]
    items = filter(check_birth, birthdays[1:])
    for item in items:
        name, month, day, flag = item.strip('\n').split()
        print name
        result = send_sms(name)
        print result
    return True


if __name__ == '__main__':
    main()
