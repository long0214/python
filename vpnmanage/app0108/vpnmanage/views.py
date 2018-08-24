from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import VpnList
import json

# Create your views here.

def get(request, query):
    field_name = [ "ID", "账号", "vpn-ip", "vpn2-ip", "项目", "使用人", "电话", "绑定MAC" ]
    if request.method == 'GET':
        if request.GET.get('query'):
            query1 = request.GET.get('query')
        else:
            query1 = 'all'
        vpnlist = []
        if query == 'all':
            for i in VpnList.objects.all():
                item = model_to_dict(i)
                vpnlist.append(item)
        # 过滤项目名称是否为null
        if query == 'used':
            for i in VpnList.objects.filter(project_name__isnull=False):
                item = model_to_dict(i)
                vpnlist.append(item)
        
        if query == 'unused':
            for i in VpnList.objects.filter(project_name__isnull=True):
                item = model_to_dict(i)
                vpnlist.append(item)
        return JsonResponse({"field_name": field_name, "vpnlist": vpnlist})
    else:
        result['message'] = "method is not support"
        result['code'] = 4
        return JsonResponse(result)

# 申请
def add(request):
    if request.method == 'POST':
        # 初始化返回的json
        result = {}
        result['message'] = 'success'
        result['code'] = 0
        data = json.loads(request.body)
        if not data:
            result['message'] = "post data is null"
            result['code'] = 4
            return JsonResponse(result)
        print(data)
        for i in data:
            # 判断是否存在
            if VpnList.objects.filter(id=i['id']):
                vpn = VpnList.objects.get(id=i['id'])
                # 判断是否未使用
                if vpn.project_name != None: 
                    result['message'] = "vpn " + str(i['id']) + " is already used"
                    result['code'] = 1
                    return JsonResponse(result)
            else:
                result['message'] = str(i['id']) + 'vpn is not exists!'
                result['code'] = 1
                return JsonResponse(result)
        
        # 存在且未使用就添加
        for i in data:
            fields_name = ["project_name", "user", "phone_number", "bind_mac"]
            for field in fields_name:
                if i[field] == '':
                    setattr(vpn, field, None)
                else:
                    setattr(vpn, field, i[field])
            try:
                vpn.save()
            except Exception:
                result['message'] = 'save failed'
                result['code'] = 1
    else:
        result['message'] = "method is not support"
        result['code'] = 4
    return JsonResponse(result)



# 回收
def delete(request):
    if request.method == 'POST':
        # 初始化返回的json
        result = {}
        result['message'] = 'success'
        result['code'] = 0
        # 获取post数据,查询数据库并重置
        data = json.loads(request.body)
        if not data:
            result['message'] = "data is null"
            result['code'] = 4
            return JsonResponse(result)
        print(data)
        for i in data:
            if VpnList.objects.filter(id=i['id']):
                vpn = VpnList.objects.get(id=i['id']) # 以主键查询
                # 重置
                fields_name = ["project_name", "user", "phone_number", "bind_mac"]
                for field in fields_name:
                    setattr(vpn, field, None)
                try:
                    vpn.save()
                except Exception:
                    result['message'] = 'save failed'
                    result['code'] = 1
            else:
                result['message'] = "this vpn is not exists!"
                result['code'] = 1
    else:
        result['message'] = "method is not support"
        result['code'] = 4
    return JsonResponse(result)

