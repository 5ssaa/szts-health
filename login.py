import json
from typing import Collection
#import urllib.request,urllib.parse,urllib.error
from urllib.parse import urlencode
import http.cookiejar
import hashlib
import requests

login_url='https://tech.szts.org.cn/WXSchoolApp/School/ClientUserBind/DoApiUserBind'
query_url='https://tech.szts.org.cn/WXCForm/ComApi/PostObject'

school_localtion='广东省深圳市福田区福田街道福民社区福强路1007号'
school_xyz='114.075996,22.531766'

apitoken=''#填写抓包获取到的微信apitoken
#因为是由微信绑定，所以登录只要token正确就可以，不用账号密码登录，再完成第一次binding后，第二次使用不需要binding

headers={
    'Connection':'close',
    'Accept':'application/json, text/plain, */*',
    'apitoken':apitoken,
    'Origin':'https://tech.szts.org.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6305002c)',
    'isajax':'1',
    'Content-Type':'application/json;charset=UTF-8',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Dest':'empty',
    'Referer':'https://tech.szts.org.cn/WXSchoolApp/dist/index.html',
    'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}


username=''#用户名
password=''#密码
md5_password=hashlib.md5(password.encode('utf-8')).hexdigest()


def binding():
    global name,userid,deptname,BZR
    post_data={
        'userid':username,
        'pwd':md5_password
    }
    post_json=json.dumps(post_data)
    login_req=requests.post(login_url,data=post_json.encode('utf-8'),headers=headers)
    text=json.loads(login_req.text)
    if('name' in text):
        name=text['name']
        userid=text['userid']
        stuObj=text['stuObj']
        deptname=stuObj['BJMC']
        BZR=stuObj['BZR']
        print('用户:'+name)
        print('学号:'+userid)
        print('班级:'+deptname)
        print('班主任:'+BZR)
        return name
    else:
        exit('登陆失败')
    
def get_CollectID():
    global CollectID
    post_data={
        "apiName":"apiCForm.GetFormCollectData"
    }
    post_json=json.dumps(post_data)
    req=requests.post(query_url,data=post_json.encode('utf-8'),headers=headers)
    CollectID=req.text[req.text.find('id')+5:req.text.find(',',(req.text.find('id')))-1]

def get_datas():
    post_data={
        "apiName":"apiCForm.GetTodayCollectDetail",
        "collectId":CollectID
    }
    post_json=json.dumps(post_data)
    req=requests.post(query_url,data=post_json.encode('utf-8'),headers=headers)
    #print(req.text)

def send():
    post_data={
        "apiName":"apiCForm.SubmitCollectForm","jsonData":"{\"CF_ID\":\"\",\"recordId\":\"\",\"collectId\":\""+CollectID+"\",\"rangeType\":2,\"userId\":\""+userid+"\",\"deptId\":0,\"deptName\":\""+deptname+"\",\"fields\":[{\"code\":\"XH\",\"value\":\""+userid+"\"},{\"code\":\"XM\",\"value\":\""+name+"\"},{\"code\":\"BJ\",\"value\":\""+deptname+"\"},{\"code\":\"BZR\",\"value\":\""+BZR+"\"},{\"code\":\"SZWZ\",\"value\":\""+school_localtion+"\"},{\"code\":\"SZWZ_LngLat\",\"value\":\""+school_xyz+"\"},{\"code\":\"DQSZCS\",\"value\":\"广东-广东省深圳市\"},{\"code\":\"ZSXXZZ\",\"value\":\"鹏城技师学院\"},{\"code\":\"STZK\",\"value\":\"[{\\\"text\\\":\\\"正常\\\"}]\"},{\"code\":\"JTCYJKZK\",\"value\":\"[{\\\"text\\\":\\\"全家身体无异常\\\"}]\"},{\"code\":\"FYSJ\",\"value\":\"[{\\\"text\\\":\\\"已在深\\\"}]\"},{\"code\":\"FYFS\",\"value\":\"[{\\\"text\\\":\\\"未离深\\\"}]\"},{\"code\":\"QJSDSDXC\",\"value\":\"无\"},{\"code\":\"JRSPJCGZGFXDQRY\",\"value\":\"[{\\\"text\\\":\\\"否\\\"}]\"},{\"code\":\"SFJCBL\",\"value\":\"[{\\\"text\\\":\\\"否\\\"}]\"},{\"code\":\"ELEYN1Y1RHLSQK\",\"value\":\"\"},{\"code\":\"ZJLCHSJCQK\",\"value\":\"\"},{\"code\":\"DYCJCSJ\",\"value\":\"\"},{\"code\":\"DYCJCJG\",\"value\":\"\"},{\"code\":\"DECJCSJ\",\"value\":\"\"},{\"code\":\"DECJCJG\",\"value\":\"\"},{\"code\":\"TSQKYM\",\"value\":\"\"},{\"code\":\"BRCNYSHDZSWMBLBPZHGZ\",\"value\":\"[{\\\"text\\\":\\\"是\\\"}]\"},{\"code\":\"DLSJ\",\"value\":\"\"},{\"code\":\"QWD\",\"value\":\"\"}]}"
    }
    
    post_json_data=json.dumps(post_data,ensure_ascii=False)
    #print(post_json_data)
    req=requests.post(query_url,data=post_json_data.encode('utf-8'),headers=headers)
    print(req.text.encode('utf-8').decode())


binding()
get_CollectID()
get_datas()
send()