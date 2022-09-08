import requests
from loguru import logger
from time import sleep

from dotenv_utils import get_api_id


def print_access_token_getting_url():
    print(f"https://oauth.vk.com/authorize?client_id={get_api_id()}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope[]=friends&scope[]=photos&response_type=token&v=5.131")
