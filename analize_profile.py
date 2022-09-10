

from profile_actions import ProfileActions


class ProfileAnalizer:

    def __init__(self, access_token):
        self.api_wrapper = ProfileActions(access_token)

    def get_friends(self, user_id):
        return self.api_wrapper.get_friends(user_id)

    def get_likes
