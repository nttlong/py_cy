import cy_kit



@cy_kit.container()
class webs:

    class sevices:
        import sample.services.users
        users:sample.services.users.Users
        user2=cy_kit.instance(sample.services.users.Users)