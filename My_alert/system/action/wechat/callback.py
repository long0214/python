from system import app
from system import jsonify
from system import request
from system import cache
from system import wechat_config
from system import Mongodb
from system.tools import SendMessage
from system.tools.Project import project
from system.models.alert_history import alert_history
import json
import xml.etree.cElementTree as ET
import re

from .callbacklib.WXBizMsgCrypt import WXBizMsgCrypt
# Create your views here.

sToken = wechat_config['Callback']['sToken']
sEncodingAESKey = wechat_config['Callback']['sEncodingAESKey']
sCorpID = wechat_config['CorpID']
wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)

@app.route('/wechat/callback.action', methods=['GET', 'POST'])
def callback():
    # 验证URL有效性
    if request.method == 'GET':
        sVerifyMsgSig = request.args.get("msg_signature")
        sVerifyTimeStamp = request.args.get("timestamp")
        sVerifyNonce = request.args.get("nonce")
        sVerifyEchoStr = request.args.get("echostr")
        ret,sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
        print(ret,'\t',sEchoStr)
        return sEchoStr
    if request.method == 'POST':
        sReqMsgSig = request.args.get('msg_signature')
        sReqTimeStamp = request.args.get("timestamp")
        sReqNonce = request.args.get("nonce")
        sReqData = request.get_data()
        # 解密数据
        ret,sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        if ret == 0:
            xml_tree = ET.fromstring(sMsg)
            MsgType = xml_tree.find("MsgType").text
            FromUserName = xml_tree.find("FromUserName").text
            if MsgType == "text":
                ToUserName =  xml_tree.find("ToUserName").text
                ConTent = xml_tree.find("Content").text
                try:
                    alertid = int(ConTent)
                    messages = alert_history.query.filter(alert_history.alert_id==alertid)
                    if messages.count() == 0:
                        SendMessage.send('Callback', FromUserName + ",你瞅啥！", touser=FromUserName)
                        return 'someone test'
                    else:
                        messages = [ item.to_json() for item in messages ]
                        for message in messages:
                            res = SendMessage.send('Callback', message['alert_message'], touser=FromUserName)
                            print(FromUserName, '\t', res)
                except Exception as e:
                    res = SendMessage.send('Callback', ConTent, touser=FromUserName)
                    print(FromUserName, '\t', ConTent.encode())
            else:
                print(FromUserName, '\t', MsgType)
                res = SendMessage.send('Callback', "what's up, man?", touser=FromUserName)
                print(FromUserName, '\t', res)
        else:
            print(ret)
            print('Decrypt failed')
            return 'Decrypt failed'
        return 'hello'

