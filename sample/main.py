import cy_kit
import sample.services.users

class FX(dict):
    def get(self, __key):
        return 1
    def __getnewargs__(self):
        print("Ok")
def test(a):
    print("OK")
fx=test(**FX(a=1))
users :sample.services.users.Users = cy_kit.inject(sample.services.users.Users)
user =users.get_user_by_username(db_name="test",username="testuser")