from dotenv import load_dotenv
import os
from pathlib import Path


def get_project_root():
    return Path(__file__).parent


def get_env_path():
    return os.path.join(get_project_root(), '.env')


def load_env():
    load_dotenv(get_env_path())


load_env()


def get_access_token():
    return os.environ.get("ACCESS_TOKEN")


def get_api_id():
    return os.environ.get("API_ID")


def get_host():
    return os.environ.get("APP_HOST")


def get_port():
    return os.environ.get("APP_PORT")


if __name__ == "__main__":
    print(get_project_root())
