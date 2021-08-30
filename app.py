from flask import Flask
from flask_login import LoginManager
from service import *
from service import Account
from controller import *
from repo.manager import SQLManager
from controller import loginApp_api, fileApp_api, searchApp_api
from config.config import get_yaml_config

app = Flask(__name__)

# set config
app_config = get_yaml_config('app_config')
app.config.from_mapping(app_config)

login_manager = LoginManager()
login_manager.init_app(app)

api2prefix = [
    (loginApp_api, '/loginApp'),
    (fileApp_api, '/fileApp'),
    (searchApp_api, '/searchApp'),
]
for api, prefix in api2prefix:
    app.register_blueprint(api, url_prefix=prefix)


def get_user(user_id):
    a = SQLManager()
    sql = "SELECT * FROM dbo.account WHERE account_name = \'" + user_id + "\'"
    a.cursor.execute(sql)
    data = a.cursor.fetchone()
    return data


@login_manager.user_loader
def user_loader(user_id):
    aa = get_user(user_id)
    if aa is not None:
        current_user = Account(aa[1], aa[3], aa[2])
        current_user.id = aa[0]
        return current_user
    return None


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
