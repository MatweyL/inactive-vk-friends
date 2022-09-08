from re import S
import vk

from dotenv_utils import get_access_token
from utils import print_access_token_getting_url

class ProfileAnalizer:

    def __init__(self, access_token):
        self.access_token = access_token
        self.vk_api = vk.API(access_token=access_token, v="5.131")


    def resolve_screen_name(self, screen_name):
        return self.vk_api.utils.resolveScreenName(screen_name=screen_name)

    def is_user_profile_accessable(self, user_id):
        user_info = self.vk_api.users.get(user_ids=user_id, fields="blacklisted, is_friend")[0]
        if (user_info.get('deactivated') or
            user_info["blacklisted"] != 0 or
            user_info["is_closed"] == True and user_info['is_friend'] == 0):
            return False
        return True



if __name__ == "__main__":
    try:
        pa = ProfileAnalizer(get_access_token())
        user_id = pa.resolve_screen_name("id431906877")['object_id']
        print(pa.is_user_profile_accessable(user_id))
    except vk.exceptions.VkAPIError as e:
        print(e)
        print_access_token_getting_url()