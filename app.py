import flask
from flask import Flask
from model import *
from controller import *
from controller import loginApp_api, fileApp_api

app = Flask(__name__)

api2prefix = [
    (loginApp_api, '/loginApp'),
    (fileApp_api, '/fileApp'),
]
for api, prefix in api2prefix:
    app.register_blueprint(api, url_prefix=prefix)

if __name__ == '__main__':
    app.run(host='localhost', port = 5000 )