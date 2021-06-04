import qrcode
import requests
import json


# 获取access_token,100分钟刷新一次
from six import BytesIO


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
def get_media_ID(path):
    img_url = 'https://api.weixin.qq.com/cgi-bin/material/add_material'
    payload_img = {
        'access_token': token,
        'type': 'image'
    }
    data = {'media': open(path, 'rb')}
    r = requests.post(url=img_url, params=payload_img, files=data)
    dict = r.json()
    return dict['media_id']


img_qr = qrcode.make('sdnjnoinoniioadxx')
# buf = BytesIO()
# # img_qr.save(buf)
# # image_stream = buf.getvalue()
img_qr.save('./qr.jpg')
token = get_token()
# token='38_xK_TbmpV6j7MT76KS_z_Xi3ABwIis3q50mFPPrOgS1Qm_itQh-BoSYRsXKmvW1kCusWtf0k-d_W2dwDeJF4RDqZRA-fhYNr_f0pEWxL2OCopL1lMwMm0IUz3esavkOEhFp9z16kDG3l7SZHHRSJeAFAFGX'

get_media_ID('./qr.jpg')

# 获取素材列表------------------------------
url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=" + token
datas = {
    "type": "image",
    "offset": 0,
    "count": 20
}
data = json.dumps(datas)
a = requests.post(url=url, data=data)
print(a.text)
