import time
import vk

from dotenv_utils import get_access_token


def correct_request(func):

    def wrapper(*args, **kwargs):
        time.sleep(0.34)
        return func(*args, **kwargs)

    return wrapper


@correct_request
def get_friends(vk_api):
    print(vk_api.friends.get(user_id=8447602))


def main():
    vk_api = vk.API(access_token=get_access_token(), v="5.131")
    get_friends(vk_api)

if __name__ == "__main__":
    main()
