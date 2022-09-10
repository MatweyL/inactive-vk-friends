from analize.profile_actions import ProfileActions
from analize.utils import print_object


class ProfileAnalizer:

    def __init__(self):
        self.api_wrapper = ProfileActions()

    def is_user_profile_accessable(self, user_id: int = None, screen_name: str = None):
        user_info = self.api_wrapper.get_user_info(user_id=user_id, screen_name=screen_name)
        if (not user_info or
            user_info.get('deactivated') or
            user_info["blacklisted"] != 0 or
            user_info["is_closed"] == True and user_info['is_friend'] == 0):
            return False
        return True

    def get_friends(self, username) -> list[int]:
        user_id = self.api_wrapper.get_id_from_screen_name(username)
        return self.api_wrapper.get_friends(user_id)

    def get_photos_liked_users(self, username, detailed=False) -> dict:
        photos_liked_users = {}
        user_id = self.api_wrapper.get_id_from_screen_name(username)
        photos = self.api_wrapper.get_photos(user_id)
        photos_liked_users["photos_count"] = len(photos)
        photos_liked_users["detailed"] = detailed
        for photo in photos:
            photo_liked_users = self.api_wrapper.get_item_liked_users(user_id=user_id, type='photo', item_id=photo['id'])
            for photo_liked_user in photo_liked_users:
                if detailed:
                    if not photos_liked_users.get(photo_liked_user):
                        photos_liked_users[photo_liked_user] = []
                    post_id = photo.get('post_id')
                    photos_liked_users[photo_liked_user].append((photo['id'], 'photo', post_id))
                else:
                    if not photos_liked_users.get(photo_liked_user):
                        photos_liked_users[photo_liked_user] = 0
                    photos_liked_users[photo_liked_user] += 1
        return photos_liked_users

    def get_unliked_users(self, username, liked_users: list[int]) -> list[int]:
        friends = set(self.get_friends(username))
        return list(friends.difference(liked_users))

    def analize_by_photos(self, screen_name: str):
        result_dict = {"message": None, "success": True}
        if not self.is_user_profile_accessable(screen_name=screen_name):
            result_dict["message"] = f"Пользователь '{screen_name}' имеет закрытый профиль/удален/вы находитесь у него в черном списке/ошибка в указании id пользователя"
            result_dict["success"] = False
            return result_dict
        liked_users = self.get_photos_liked_users(screen_name)
        unliked_users_ids = self.get_unliked_users(screen_name, liked_users)
        unliked_users_profiles = self.api_wrapper.get_users_info(user_ids=unliked_users_ids)
        result_dict["message"] = f"Найдено {len(unliked_users_ids)} пользователей, не проявивших активности"
        result_dict["unliked_users_profiles"] = unliked_users_profiles
        return result_dict

            


if __name__ == "__main__":
    pa = ProfileAnalizer()
    username = "lomchik_m"
    if pa.is_user_profile_accessable(screen_name=username):
        liked_users = pa.get_photos_liked_users(username)
        unliked_users = pa.get_unliked_users(username, liked_users)
        for user_id in unliked_users:
            print(f"https://vk.com/id{user_id}")
