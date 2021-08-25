from flask import Flask
from flask_login import LoginManager, current_user, login_required
from service import *
from service import Account
from controller import *
from controller import loginApp_api, fileApp_api, SearchApp_api

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

api2prefix = [
    (loginApp_api, '/loginApp'),
    (fileApp_api, '/fileApp'),
    (SearchApp_api, '/SearchApp'),
]
for api, prefix in api2prefix:
    app.register_blueprint(api, url_prefix=prefix)


def get_user(user_id):
    u = 'tmp'#get user in db
    return u

@login_manager.user_loader
def user_loader(user_id):
    aa = get_user(user_id)
    if aa is not None:
        current_user = Account()
        current_user = aa

        return current_user
    return None

if __name__ == '__main__':
    app.run(host='localhost', port = 5000,debug=True )