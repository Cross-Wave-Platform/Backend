import os
import yaml

CWD = os.path.abspath(os.getcwd())

def dump_config(conf_dict,dir_path):
    with open(os.path.join(dir_path,'config.yaml'),'w') as conf_file:
        yaml.dump(conf_dict,conf_file,default_flow_style=False)

# create dir if no exists
def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# repo/config.yaml
TMP_DIR_PATH = os.path.join(CWD,'tmp_dir')

repo_config = {
    "mymssql": {
        "host": "localhost",
        "user": "SA",
        "password": "Kit2021db",
        "database": "KIT_DB"
    },
    "tmp_dir": TMP_DIR_PATH
}

REPO_PATH = os.path.join(CWD,'repo')
dump_config(repo_config,REPO_PATH)

create_dir(TMP_DIR_PATH)

# service/config.yaml
UPLOAD_PATH = os.path.join(CWD,'upload')
DOWNLOAD_PATH = os.path.join(CWD,'download')

service_config = {
    "upload_dir": UPLOAD_PATH,
    "download_dir": DOWNLOAD_PATH
}

SERVICE_PATH = os.path.join(CWD,'service')
dump_config(service_config,SERVICE_PATH)

create_dir(UPLOAD_PATH)
create_dir(DOWNLOAD_PATH)