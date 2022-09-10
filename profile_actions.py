import vk
import time

from dotenv_utils import get_access_token
from utils import print_access_token_getting_url, print_object


def correct_request(func):
    base_timeout = 0.3
    def wrapper(*args, base_timeout=base_timeout, **kwargs):
        time.sleep(base_timeout)
        start = time.time()
        result =  func(*args, **kwargs)
        exec_time = round(time.time() - start, 4)
        print(f"{func.__name__}: execution: {exec_time} s; sleep: {base_timeout} s; total: {exec_time + 0.3} s")
        return result

    return wrapper

class ProfileActions:

    def __init__(self):
        self.vk_api = vk.API(access_token=get_access_token(), v="5.131")

    @correct_request
    def get_id_from_screen_name(self, screen_name):  # need to add cache .sqlite3 to decrease api requests
        return self.vk_api.utils.resolveScreenName(screen_name=screen_name)['object_id']

    @correct_request
    def get_user_info(self, user_id: int = None, screen_name: str = None, fields="blacklisted, is_friend"):
        using_id=None
        if user_id:
            using_id = user_id
        else:
            using_id = screen_name
        user_info =  self.vk_api.users.get(user_ids=using_id, fields=fields)
        if user_info:
            return user_info[0]
        return None

    @correct_request
    def get_users_info(self, user_ids: list[int], fields="photo_100"):
        users_info = self.vk_api.users.get(user_ids=user_ids, fields=fields)
        return users_info
    
    @correct_request
    def get_wall_media(self, user_id, count=100):
        return self.vk_api.wall.get(owner_id=user_id, count=count)['items']

    @correct_request
    def get_photos(self, user_id, count=100):
        return self.vk_api.photos.getAll(owner_id=user_id, count=count)['items']

    @correct_request
    def get_item_liked_users(self, user_id, type, item_id):
        return self.vk_api.likes.getList(type=type, owner_id=user_id, item_id=item_id)['items']

    @correct_request
    def get_friends(self, user_id):
        return self.vk_api.friends.get(user_id=user_id)['items']


if __name__ == "__main__":
    try:
        pa = ProfileActions()
        print(pa.get_users_info("lomchik_m"))
    except vk.exceptions.VkAPIError as e:
        print(e)
        print_access_token_getting_url()


