from loguru import logger
from time import sleep

from dotenv_utils import get_api_id


def print_access_token_getting_url():
    print(f"https://oauth.vk.com/authorize?client_id={get_api_id()}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope[]=friends&scope[]=photos&response_type=token&v=5.131")


def print_object(obj, offset=0):
    if isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, str):
        print(f"{offset * '    '}{obj}")
    elif isinstance(obj, dict):
        print(f"{offset * '    '}", "{", sep='')
        for key in obj:
            print(f"{offset * '    '}{key}:")
            print_object(obj[key], offset + 1)
        print(f"{offset * '    '}", "}", sep='')
    elif isinstance(obj, list):
        print(f"{offset * '    '}", "[", sep='')
        for elem in obj:
            print_object(elem, offset)
        print(f"{offset * '    '}", "]", sep='')
    elif isinstance(obj, set) or isinstance(obj, tuple):
        print(f"{offset * '    '}", "(", sep='')
        for elem in obj:
            print_object(elem, offset)
        print(f"{offset * '    '}", ")", sep='')
    else:
        print(f"{offset * '    '}{obj}")
        