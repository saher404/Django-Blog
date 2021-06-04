import requests


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


token = get_token()
print(token)
