import cy_kit
import sample.services.users
class User2:
    def __init__(self):
        print("OK")


cy_kit.config_provider(
    sample.services.users.Users,
    User2
)
fx= User2()
fx.create_user()
sevice:sample.services.users.Users=sample.webs.sevices.users
fx=sample.webs.sevices.user2.get_me()==sample.webs.sevices.users.get_me()
sevice.get_user_by_username('a','b')
