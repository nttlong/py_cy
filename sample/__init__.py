import cy_kit
import sample.services.users
class User2:
    def __init__(self):
        pass

    def get_user_by_username(self, db_name, username):
        return "test"
    def get_me(self):
        return self



    def create_user(self):
        raise NotImplemented


@cy_kit.container()
class webs:

    class sevices:

        users: sample.services.users.Users
        user2=cy_kit.scope(sample.services.users.Users)
        user3 = cy_kit.scope(sample.services.users.Users)