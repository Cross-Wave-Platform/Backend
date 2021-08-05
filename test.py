import requests
import jwt
from controller.utils.response import HTTPError, HTTPResponse
from controller.utils.request import Request
from service.utils import hash_id
from functools import wraps
from service.account import Account, jwt_decode

from datetime import datetime, timedelta
import os

JWT_EXP = timedelta(days=int(os.environ.get('JWT_EXP', '30')))
JWT_ISS = os.environ.get('JWT_ISS', 'test.test')
JWT_SECRET = os.environ.get('JWT_SECRET', 'SuperSecretString')

if __name__ == "__main__":
    username = 'testuser'
    password = 'testpassword'
    user = hash_id(username, password)

    ppl = {"userId": username,"username":"test" , "iss": JWT_ISS, "secret":"test"}
    encoded_jwt = jwt.encode(ppl, JWT_SECRET, algorithm="HS256")
    #print(encoded_jwt)


    cookie = 'piann='+encoded_jwt

    cookie_para = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    url = 'http://127.0.0.1:5000/loginApp/test'
    headers = { 'Host':'example.com',
                    'Connection':'keep-alive',
                    'Cache-Control':'max-age=0',
                    'Accept': 'text/html, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
                    'DNT':'1',
                    'Referer': 'http://example.com/',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'
}

    print(cookie_para)
    de = jwt_decode(encoded_jwt)
    print(de)
'''
    response = requests.get(url=url, cookies=cookie_para, headers=headers)
    print(response.content.decode())
    #print(r.status)
'''