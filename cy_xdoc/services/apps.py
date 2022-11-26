import datetime
import uuid

import cy_docs
import cy_kit
from cy_xdoc.services.base import Base,DbConnect
from cy_xdoc.models.apps import App


class AppServices:

    def __init__(self,db=cy_kit.inject(DbConnect)):
        self.db_context:DbConnect=db
    def get_list(self, app_name: str):
        docs = self.db_context.db(app_name).doc(App)
        ret = docs.context.aggregate().project(
            cy_docs.fields.AppId >> docs.fields._id ,
            docs.fields.name,
            docs.fields.description,
            docs.fields.domain,
            docs.fields.login_url,
            docs.fields.return_url_afterSignIn

        ).sort(
            docs.fields.Name.asc(),
            docs.fields.RegisteredOn.desc()
        )
        return ret

    def get_item(self, app_name, app_get):
        docs = self.db_context.db(app_name).doc(App)
        return docs.context.aggregate().project(
            cy_docs.fields.AppId >> docs.fields.Id ,
            docs.fields.Name,
            docs.fields.description,
            docs.fields.domain,
            docs.fields.login_url,
            docs.fields.return_url_afterSignIn

        ).match(docs.fields.Name == app_get).first_item()

    def create(self,
               Name: str,
               Description: str,
               Domain: str,
               LoginUrl: str,
               ReturnUrlAfterSignIn: str,
               UserName: str,
               Password: str):
        doc = self.expr(App)
        app_id = str(uuid.uuid4())
        secret_key = str(uuid.uuid4())
        self.db('admin').doc(App).insert_one(
            doc.Id << app_id,
            doc.Name << Name,
            doc.ReturnUrlAfterSignIn << ReturnUrlAfterSignIn,
            doc.Domain << Domain,
            doc.LoginUrl << LoginUrl,
            doc.Description << Description,
            doc.Username << UserName,
            doc.Password << Password,
            doc.SecretKey << secret_key,
            doc.RegisteredOn << datetime.datetime.utcnow()

        )
        ret = cy_docs.DocumentObject(
            AppId=app_id,
            Name=Name,
            ReturnUrlAfterSignIn=ReturnUrlAfterSignIn,
            Domain=Domain,
            LoginUrl=LoginUrl,
            Description=Description,
            Username = UserName,
            SecretKey = secret_key,
            RegisteredOn= datetime.datetime.utcnow()
        )
        return ret

    def create_default_app(self,domain:str,login_url:str,return_url_after_sign_in:str):
        document=self.db_context.db('admin').doc(App)
        default_amdin_db = self.db_context.admin_db_name
        application = document.context @ (document.fields.Name==default_amdin_db)
        if application is None:
            document.context.insert_one(
                document.fields.Name<<default_amdin_db,
                document.fields.Domain<<domain,
                document.fields.RegisteredOn<<datetime.datetime.utcnow(),
                document.fields.LoginUrl<<login_url,
                document.fields.ReturnUrlAfterSignIn<<return_url_after_sign_in
            )
