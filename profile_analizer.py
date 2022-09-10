from re import S
import vk

from dotenv_utils import get_access_token
from utils import print_access_token_getting_url, print_object

class ProfileAnalizer:

    def __init__(self, access_token):
        self.access_token = access_token
        self.vk_api = vk.API(access_token=access_token, v="5.131")


    def resolve_screen_name(self, screen_name):
        """
        return {'object_id': 12345678, 'type': 'user'}
        """
        return self.vk_api.utils.resolveScreenName(screen_name=screen_name)

    def is_user_profile_accessable(self, user_id):
        user_info = self.vk_api.users.get(user_ids=user_id, fields="blacklisted, is_friend")[0]
        if (user_info.get('deactivated') or
            user_info["blacklisted"] != 0 or
            user_info["is_closed"] == True and user_info['is_friend'] == 0):
            return False
        return True
    
    def get_wall_media(self, user_id, count=100):
        items = self.vk_api.wall.get(owner_id=user_id, count=count)
        return items

    def get_wall_liked_users(self, user_id, count):
        liked_users = {}
        wall_media = self.get_wall_media(user_id, count=count)
        for post in wall_media['items']:
            current_post_liked_users = self.vk_api.likes.getList(type=post['post_type'], owner_id=user_id, item_id=post['id'])['items']
            for user in current_post_liked_users:
                if liked_users.get(user):
                    liked_users[user][0] += 1
                    liked_users[user][1].append(post['id'])
                else:
                    liked_users[user] = [1, post['id']]
        return liked_users

    def get_photos(self, user_id, count=100):
        photos = self.vk_api.photos.getAll(owner_id=user_id, count=count)
        return photos

    def get_photos_liked_users(self, user_id, count=100):
        liked_users = {}
        photos = self.get_photos(user_id, count=count)
        for photo in photos['items']:
            current_post_liked_users = self.vk_api.likes.getList(type=photo, owner_id=user_id, item_id=photo['id'])['items']
            for user in current_post_liked_users:
                if liked_users.get(user):
                    liked_users[user][0] += 1
                    liked_users[user][1].append(photo['id'])
                else:
                    liked_users[user] = [1, photo['id']]
        return liked_users
                

"""    id:
        457242927
    owner_id:
        140351546
    post_id:
        431"""


if __name__ == "__main__":
    try:
        pa = ProfileAnalizer(get_access_token())
        user_id = pa.resolve_screen_name("crave_ozer_man")['object_id']
        # print_object(pa.get_photos(user_id, count=1))
        print_object(pa.get_wall_media(user_id, count=4))
        # print(pa.is_user_profile_accessable(user_id))
    except vk.exceptions.VkAPIError as e:
        print(e)
        print_access_token_getting_url()


