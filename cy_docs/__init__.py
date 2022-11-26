import os.path
import pathlib

import bson
import pymongo.mongo_client
import ctypes
import sys
__release_mode__ = True
__working_dir__ = pathlib.Path(__file__).parent.__str__()




sys.path.append(__working_dir__)
import cy_docs_x

from typing import TypeVar, Generic, List

T = TypeVar('T')


def expr(cls: T) -> T:
    """
    Create mongodb build expression base on __cls__
    :param cls:
    :return:
    """
    ret = cy_docs_x.fields[cls]

    return ret
def get_doc(collection_name: str, client: pymongo.mongo_client.MongoClient, indexes: List[str] = [],
            unique_keys: List[str] = []):

    return getattr(cy_docs_x,"Document")(collection_name, client,indexes=indexes,unique_keys=unique_keys)
def define(name:str,indexes:List[str]=[],uniques:List[str]=[]):
    return getattr(cy_docs_x,"document_define")(name,indexes,uniques)
fields=cy_docs_x.fields
"""
For any expression
"""
def context(client, cls):
    return cy_docs_x.context(client,cls)

def concat(*args): return cy_docs_x.Funcs.concat(*args)
def exists(field):return cy_docs_x.Funcs.exists(field)
def is_null(field):return cy_docs_x.Funcs.is_null(field)
def is_not_null(field):return cy_docs_x.Funcs.is_not_null(field)
def not_exists(field):return cy_docs_x.Funcs.not_exists(field)

DocumentObject=cy_docs_x.DocumentObject


def file_get(client:pymongo.MongoClient, db_name:str, file_id):
    return cy_docs_x.file_get(client, db_name, file_id)


async def get_file_async(client, db_name, file_id):
    return await cy_docs_x.get_file_async(client,db_name,file_id)


def create_file(client:pymongo.MongoClient,db_name, file_name,content_type:str, chunk_size, file_size):
    return cy_docs_x.create_file(
        client=client,
        file_size=file_size,
        chunk_size=chunk_size,
        file_name=file_name,
        db_name=db_name,
        content_type=content_type
    )


def file_add_chunk(client :pymongo.MongoClient, db_name: str, file_id: bson.ObjectId,chunk_index:int, chunk_data: bytes):
    return cy_docs_x.file_add_chunk(
        client=client,
        db_name=db_name,
        file_id=file_id,
        chunk_index=chunk_index,
        chunk_data=chunk_data
    )