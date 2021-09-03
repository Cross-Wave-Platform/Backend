from flask import Flask
from service.account import login_manager
from controller import loginApp_api, fileApp_api, personalApp_api, searchApp_api, adminApp_api, reportApp_api
from config.config import get_yaml_config

app = Flask(__name__)

# set app config
app_config = get_yaml_config('app_config')
app.config.from_mapping(app_config)

login_manager.init_app(app)

api2prefix = [
    (loginApp_api, '/loginApp'),
    (fileApp_api, '/fileApp'),
    (personalApp_api, '/personalApp'),
    (adminApp_api, '/adminApp'),
    (searchApp_api, '/searchApp'),
    (reportApp_api, '/reportApp'),
]
for api, prefix in api2prefix:
    app.register_blueprint(api, url_prefix=prefix)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
