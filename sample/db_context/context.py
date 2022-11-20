import pymongo

import cy_docs
import cy_kit
from sample.models.users import Users
from sample.db_context.db_connect import DbConnect
from sample.models import *
from cy_docs import context
from typing import TypeVar, Generic

T=TypeVar("T")
class ContextDocument(Generic[T]):
    def __init__(self,client:pymongo.MongoClient,cls:type,db_name:str):
        self.client=client
        self.cls=cls
        self.db_name = db_name
    @property
    def fields(self) -> T:
        return cy_docs.expr(self.cls)
    @property
    def context(self):
        return cy_docs.context(self.client, self.cls)[self.db_name]

class DBContext:
    def __init__(self,connect:DbConnect=cy_kit.inject(DbConnect)):
        self.client=connect.client
    def get_doc(self,db_name:str,cls:T)->ContextDocument[T]:
        return ContextDocument[T](self.client,cls,db_name)


