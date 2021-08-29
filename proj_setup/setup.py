from pathlib import Path
import yaml

CWD = Path().resolve()
STORAGE_PATH = CWD / "storage"


def dump_config(conf_dict, dir_path):
    with open(dir_path / "config.yaml", 'w') as conf_file:
        yaml.dump(conf_dict,
                  conf_file,
                  default_flow_style=False,
                  sort_keys=False)


# create dir if no exists
def create_dir(dir_path):
    if not Path.exists(dir_path):
        Path.mkdir(dir_path, parents=True)


# app config
app_config = {"app_config": {"SECRET_KEY": "test"}}

# repo config
TMP_DIR_PATH = STORAGE_PATH / 'tmp_dir'

repo_config = {
    "mssql": {
        "host": "localhost",
        "user": "SA",
        "password": "Kit2021db",
        "database": "KIT_DB"
    },
    "tmp_dir": str(TMP_DIR_PATH)
}

create_dir(TMP_DIR_PATH)

# service config
UPLOAD_PATH = STORAGE_PATH / 'upload'
DOWNLOAD_PATH = STORAGE_PATH / 'download'

service_config = {
    "upload_dir": str(UPLOAD_PATH),
    "download_dir": str(DOWNLOAD_PATH)
}

create_dir(UPLOAD_PATH)
create_dir(DOWNLOAD_PATH)

total_config = {}
total_config.update(app_config)
total_config.update(repo_config)
total_config.update(service_config)
dump_config(total_config, CWD / "config")
