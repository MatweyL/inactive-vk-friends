import vk
import time

from dotenv_utils import get_access_token
from utils import print_access_token_getting_url, print_object


def correct_request(func):

    def wrapper(*args, **kwargs):
        time.sleep(0.34)
        return func(*args, **kwargs)

    return wrapper

class ProfileActions:

    def __init__(self, access_token):
        self.access_token = access_token
        self.vk_api = vk.API(access_token=access_token, v="5.131")

    @correct_request
    def get_id_from_screen_name(self, screen_name):
        return self.vk_api.utils.resolveScreenName(screen_name=screen_name)['object_id']

    @correct_request
    def is_user_profile_accessable(self, user_id):
        user_info = self.vk_api.users.get(user_ids=user_id, fields="blacklisted, is_friend")[0]
        if (user_info.get('deactivated') or
            user_info["blacklisted"] != 0 or
            user_info["is_closed"] == True and user_info['is_friend'] == 0):
            return False
        return True
    
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

    def get_photos_liked_users(self, user_id, count=100):
        liked_users = {}
        photos = self.get_photos(user_id, count=count)
        for photo in photos['items']:
            current_post_liked_users = self.vk_api.likes.getList(type=photo, owner_id=user_id, item_id=photo['id'])['items']
            for user in current_post_liked_users:
                if liked_users.get(user):
                    liked_users[user].append(photo['id'])
                else:
                    liked_users[user] = [photo['id']]
        return liked_users


if __name__ == "__main__":
    try:
        pa = ProfileActions(get_access_token())
        user_id = pa.get_id_from_screen_name("lomchik_m")
        # print_object(pa.get_photos(user_id, count=1))
        print_object(pa.get_videos(user_id))
        # print(pa.is_user_profile_accessable(user_id))
    except vk.exceptions.VkAPIError as e:
        print(e)
        print_access_token_getting_url()


