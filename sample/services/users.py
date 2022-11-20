import cy_kit
import sample.models.users
from sample.db_context.context import DBContext
class Users:
    def __init__(self,db_context:DBContext =cy_kit.inject(DBContext)):
        self.db_context:DBContext =db_context

    def get_user_by_username(self, db_name, username):
        doc =self.db_context.get_doc(db_name,sample.models.users.Users)
        return doc.context.find_one(
            doc.fields.Username==username
        )

