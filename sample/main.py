import cy_kit
import sample.services.users

sevice:sample.services.users.Users=sample.webs.sevices.users
fx=sample.webs.sevices.user2.get_me()==sample.webs.sevices.users.get_me()
sevice.create_user()
print(user)