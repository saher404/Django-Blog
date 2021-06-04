import requests
import re
import json


def download_MP3(url):
    '''下载歌曲'''
    r = requests.get(url)
    with open('Music\\可不可以.mp3', 'wb') as f:
        f.write(r.content)


def getUrl():
    '''获得歌曲URL'''
    r = requests.post(url, headers=headers, data=data)
    response_data = json.loads(r.text)
    print(response_data['data'][0]['url'])
    download_url = response_data['data'][0]['url']
    return download_url


if __name__ == "__main__":
    url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
        'Host': 'music.163.com',
        'referer': 'https://music.163.com/',
        'Origin': 'https://music.163.com'
    }

    data = {
        'params': 'u6SEfpt2WTDENzie0aJs1c3dzjB1cQjGVERXnkRLnHnsiFSaAdUfeBwu9jeoC6axZjvKyidX7r9S7aoPiyxJ2qJ2X+mygkjnYZM4qYvgyBZAdvqtY7OfVnuMUaAnAG4U',
        'encSecKey': 'c02c3b63f5b129b1891f516ace6e8343e848d9bd15d5494e3be9f116c2b76bc2f430837de91e9fd4eec7aa257763f1a6b6f8f6861364fb8ca77c9dbc376db203ea92ed8a8f2c225e031b581e154b8d85f409b380cf982475abe9b32d5a5d2111e69c6d3599e186fe29afa5183f7b37645395e964e656cc3e8611f559f664ee69'
    }
    url = getUrl()
    download_MP3(url)
