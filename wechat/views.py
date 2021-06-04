# import sys
# sys.path.append(r"/root/django测试/myfuck/wechat/")
# from seetaface.api import *
import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
from wechat import tyuling_replay
import re
import random
import qrcode
import base64
from aip import AipFace
import cv2

'''
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            佛祖保佑       永无BUG
'''


# django默认开启csrf防护，这里使用@csrf_exempt去掉防护
@csrf_exempt
def weixin_main(request):
    if request.method == "GET":
        # 接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        # 服务器配置中的token
        token = 'saher'
        # 把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [str(token), str(timestamp), str(nonce)]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist])
        hashstr = hashstr.encode("utf-8")
        hashstr = hashlib.sha1(hashstr).hexdigest()
        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("field")
    else:
        othercontent = autoreply(request)
        return HttpResponse(othercontent)


# 微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
import xml.etree.ElementTree as ET


def autoreply(request):
    try:
        webData = request.body
        xmlData = ET.fromstring(webData)

        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        MsgType = xmlData.find('MsgType').text
        MsgId = xmlData.find('MsgId').text

        toUser = FromUserName
        fromUser = ToUserName

        if msg_type == 'text':
            msg_content = xmlData.find('Content').text
            if msg_content == '博客':
                title = "Saher的个人博客~"
                description = "欢迎光临我的个人博客啦~目前本博客还在测试阶段，有bug请多多见谅。"
                picurl = "http://118.31.175.222/static/wechat_Img/Art1.jpg"
                url = "http://www.saher666.cn/"
                replyMsg = ArtMsg(toUser, fromUser, title, description, picurl, url)
                return replyMsg.send()
            if '二维码' in msg_content:
                content = xmlData.find('Content').text[4:]
                img_qr = qrcode.make(content)
                img_qr.save('./wechat/static/qr.jpg')  # 生成QR
                token = get_token()
                media_id = get_media_ID('./wechat/static/qr.jpg', token)
                replyMsg = ImgMsg(toUser, fromUser, media_id)
                return replyMsg.send()
            if msg_content == '二刺螈':
                media_id = imgSC()
                replyMsg = ImgMsg(toUser, fromUser, media_id)
                return replyMsg.send()
            if '机器人' in msg_content:
                content = xmlData.find('Content').text[4:]
                # 根据公众号粉丝的ID生成符合要求的图灵机器人userid
                if len(fromUser) > 31:
                    tuling_userid = str(fromUser[0:30])
                else:
                    tuling_userid = str(fromUser)
                tuling_userid = re.sub(r'[^A-Za-z0-9]+', '', tuling_userid)
                # 调用图灵机器人API返回图灵机器人返回的结果
                tuling_replay_text = tyuling_replay.get_message(content, tuling_userid)
                replyMsg = TextMsg(toUser, fromUser, tuling_replay_text)
                return replyMsg.send()
            content = "您好,欢迎来到saher的百宝箱!本公众号测试中TAT " \
                      "。\n回复“博客”即可获取我的博客链接，\n在回复开头加上“二维码：”字样即可在线生成二维码图片（例如想要生成一张含有“你好”字样的二维码，请回复“二维码：你好”），\n" \
                      "回复“二刺螈”即可获取随机福利图一张," \
                      "\n在文字回复开头加上“机器人：”字样或直接发送语言，即可体验自动聊天机器人在线陪聊。（例如：回复“机器人：你好啊”）" \
                      "\n发送一张含有人脸的图片，即可体验人工智能人脸分析功能（分析年龄、性别等）"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

        elif msg_type == 'image':
            try:
                pic_url = xmlData.find('PicUrl').text
                download(pic_url)
                baidu_face('./wechat/static/user_tp.jpg')
                token = get_token()
                media_id = get_media_ID('./wechat/static/return_user.jpg', token)
                replyMsg = ImgMsg(toUser, fromUser, media_id)
                return replyMsg.send()
            except:
                content = "图片处理出错，可能为如下原因：\n" \
                          "1.图片大小过小\n" \
                          "2.图片内未检测到人脸\n" \
                          "3.人脸未处于图片中央部分\n"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()

        elif msg_type == 'voice':
            content = xmlData.find('Recognition').text
            # 根据公众号粉丝的ID生成符合要求的图灵机器人userid
            if len(fromUser) > 31:
                tuling_userid = str(fromUser[0:30])
            else:
                tuling_userid = str(fromUser)
            tuling_userid = re.sub(r'[^A-Za-z0-9]+', '', tuling_userid)
            # 调用图灵机器人API返回图灵机器人返回的结果
            tuling_replay_text = tyuling_replay.get_message(content, tuling_userid)
            replyMsg = TextMsg(toUser, fromUser, tuling_replay_text)
            return replyMsg.send()
        elif msg_type == 'video':
            content = "视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'shortvideo':
            content = "小视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'location':
            l_x = xmlData.find('Location_X').text
            l_y = xmlData.find('Location_Y').text
            content = "位置已收到,您目前所在的经纬度为：经度" + l_y + ' 纬度' + l_x
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'event':
            event = xmlData.find('Event').text
            if event == 'subscribe':
                content = "欢迎订阅我的百宝箱，本公众号主要是交流学习各种编程知识，和分享我的一些小项目。希望你能在这里玩的开心。\n" \
                          "回复“菜单”即可查看主菜单界面。"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            content = "此功能暂未开发，请稍后尝试。"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            msg_type == 'link'
            content = "链接已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

    except Exception as Argment:
        return Argment


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


import time


# 文本型消息
class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)


# 图片型消息
class ImgMsg(Msg):
    def __init__(self, toUserName, fromUserName, media_id):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = media_id

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)


# 图文型消息
class ArtMsg(Msg):
    def __init__(self, toUserName, fromUserName, title, description, picurl, url):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['title'] = title
        self.__dict['description'] = description
        self.__dict['picurl'] = picurl
        self.__dict['url'] = url

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>1</ArticleCount>
        <Articles>
        <item>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
        <PicUrl><![CDATA[{picurl}]]></PicUrl>
        <Url><![CDATA[{url}]]></Url>
        </item>
        </Articles>
        </xml>
        """
        return XmlForm.format(**self.__dict)


# 随机生成公众号的图片id
def imgSC():
    imglist = ["K5OW_QVY34WN_hYmLJESUKX2Ka9meEB3qBBw2peqyYg", "K5OW_QVY34WN_hYmLJESUEXsdEcgWuPQcmLTxtvQE7Q",
               "K5OW_QVY34WN_hYmLJESUKkcfN16PksTUzT6l-eRGns", "K5OW_QVY34WN_hYmLJESUGPgcZsabdid4S2pViqcas8",
               "K5OW_QVY34WN_hYmLJESUKJr5qeeoBSljDq5Uv8o7Q8", "K5OW_QVY34WN_hYmLJESUKZmdmIEXedCB4WIlZSVijU",
               "K5OW_QVY34WN_hYmLJESUBS2D0GU0D2gbQookTrjloQ", "K5OW_QVY34WN_hYmLJESUCrHcX1Nbga0lQ60oIAaTPU",
               "K5OW_QVY34WN_hYmLJESUIsfWdR1q6f3fS4ShGVUq5w"]
    a = imglist[random.randint(0, len(imglist) - 1)]
    return a


# 二维码生成模块
# 获取access_token,100分钟刷新一次
def get_token():
    payload_access_token = {
        'grant_type': 'client_credential',
        'appid': 'wxb804c6877ed11a9d',
        'secret': 'c83d76a3acbc4b09a701e0360501cf83'
    }
    token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    r = requests.get(token_url, params=payload_access_token)
    dict_result = (r.json())
    return dict_result['access_token']


# 上传图片并返回media_id
def get_media_ID(path, token):
    img_url = 'https://api.weixin.qq.com/cgi-bin/material/add_material'
    payload_img = {
        'access_token': token,
        'type': 'image'
    }
    data = {'media': open(path, 'rb')}
    r = requests.post(url=img_url, params=payload_img, files=data)
    dict = r.json()
    return dict['media_id']


# 指定url文件下载(图片回复功能）

def download(url):
    req = requests.get(url)
    filename = './wechat/static/user_tp.jpg'
    if req.status_code != 200:
        print('下载异常')
        return
    try:
        with open(filename, 'wb') as f:
            # req.content为获取html的内容
            f.write(req.content)
            print('下载成功')
    except Exception as e:
        print(e)


# 百度API人脸识别
def baidu_face(img_path):
    # 配置百度aip参数
    APP_ID = '22856265'
    API_KEY = 'BFmUvGfiGW31l5jehY043bmz'
    SECRET_KEY = 'waHP5vKa7xhV2MDQt27UUe2PtvZej5yk'
    a_face = AipFace(APP_ID, API_KEY, SECRET_KEY)
    image_type = 'BASE64'

    options = {'face_field': 'age,gender,beauty', "max_face_num": 10}
    max_face_num = 10

    def get_file_content(file_path):
        """获取文件内容"""
        with open(file_path, 'rb') as fr:
            content = base64.b64encode(fr.read())
            return content.decode('utf8')

    def face_score(file_path):
        """脸部识别分数"""
        result = a_face.detect(get_file_content(file_path), image_type, options)
        return result

    # 图片地址，图片与程序同一目录下
    file_path = img_path
    result = face_score(file_path)
    # #从文件读取图像并转为灰度图像
    img = cv2.imread(file_path)
    # 图片放文字
    # 设置文件的位置、字体、颜色等参数
    font = cv2.FONT_HERSHEY_DUPLEX
    # font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")
    color = (0, 0, 255)
    for item in result['result']['face_list']:
        x = int(item['location']['left'])
        y = int(item['location']['top'])
        w = item['location']['width']
        h = item['location']['height']
        age = item['age']
        beauty = item['beauty']
        gender = item['gender']['type']
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
        cv2.putText(img, 'age:%s' % age, (x, y + h + 70), font, 2, color, 3)
        cv2.putText(img, 'beauty:%s' % beauty, (x, y + h + 140), font, 2, color, 3)
        cv2.putText(img, 'gender:%s' % gender, (x, y + h + 210), font, 2, color, 3)

    cv2.imwrite('./wechat/static/return_user.jpg', img)
# # 人脸识别(Linux内核无法运行项目)
# def seetaface_age(url):
#     """ 检测一张大图中的每个人脸的年龄 """
#     init_mask = FACE_DETECT | LANDMARKER5 | FACE_AGE
#     seetaFace = SeetaFace(init_mask)  # 初始化引擎
#     print(seetaFace)
#     image = cv2.imread(url)
#     detect_result = seetaFace.Detect(image)
#     for i in range(detect_result.size):
#         face = detect_result.data[i].pos
#         c_image = image[face.y:face.y + face.height, face.x:face.x + face.width]
#         points_5 = seetaFace.mark5(image, face)
#         age = seetaFace.PredictAgeWithCrop(image, points_5)
#         return age

# #见imgup.py
# # 获取access_token,100分钟刷新一次
# def get_token():
#     payload_access_token = {
#         'grant_type': 'client_credential',
#         'appid': 'wxb804c6877ed11a9d',
#         'secret': 'c83d76a3acbc4b09a701e0360501cf83'
#     }
#     token_url = 'https://api.weixin.qq.com/cgi-bin/token'
#     r = requests.get(token_url, params=payload_access_token)
#     dict_result = (r.json())
#     return dict_result['access_token']
#
#
# # 上传图片并返回media_id
# def get_media_ID(path):
#     img_url = 'https://api.weixin.qq.com/cgi-bin/material/add_material'
#     payload_img = {
#         'access_token': get_token(),
#         'type': 'image'
#     }
#     data = {'media': open(path, 'rb')}
#     r = requests.post(url=img_url, params=payload_img, files=data)
#     dict = r.json()
#     return dict['media_id']
#
#
# # 获取素材列表------------------------------
# import requests
# import json
#
# url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=yourtoken"
#
# datas = {
#     "type": "image",
#     "offset": 0,
#     "count": 20
# }
# data = json.dumps(datas)
# a = requests.post(url=url, data=data)
# print(a.text)
