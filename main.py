from analize.profile_actions import ProfileActions
from analize.utils import print_access_token_getting_url, print_object
from app.views import run_flask


def main():
    print_access_token_getting_url()
    run_flask()


if __name__ == "__main__":
    main()
