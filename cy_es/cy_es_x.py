import datetime
import inspect
import json
import os
import typing
import uuid

import elasticsearch.exceptions
from elasticsearch import Elasticsearch
from typing import List
import pydantic


def get_all_index(client: Elasticsearch) -> List[str]:
    return list(client.indices.get_alias("*").keys())


def __make_up_es_syntax_depriciate__(field_name: str, value):
    if '.' not in field_name:
        return {"term": {field_name: value}}
    else:
        path = ""
        items = field_name.split('.')
        for i in range(0, items.__len__() - 1):
            path += items[i] + "."
        path = path[:-1]
        return {
            "nested": {
                "path": items[0],
                "query": {
                    "term": {field_name: value}
                }
            }
        }


def __make_up_es_syntax__(field_name: str, value):
    if type(value) == list:
        """
        "terms_set": {
      "programming_languages": {
        "terms": [ "c++", "java", "php" ],
        "minimum_should_match_field": "required_matches"
      }
    }
        """
        return {
            "terms_set": {
                field_name: {
                    "terms": value,
                    "minimum_should_match_script": {
                        "source": f"Math.min(params.num_terms, {value.__len__()})"
                    },
                }
            }

        }
    """
     return {
                    "terms":  {field_name: value},
                    "minimum_should _match": value.__len__()
                }
    """
    return {"term": {field_name: value}}


def __make_up_es1__(field_name: str, value):
    items = field_name.split('.')
    if items.__len__() == 1: return {field_name: value}
    ptr = {}
    ret = ptr

    n = items.__len__()
    for i in range(0, n):
        index = n - i - 1
        ptr[items[index]] = {}
        ptr = ptr[items[index]]
    ptr[items[n - 1]] = {"value": value}
    return ret


class DocumentFields:
    def __init__(self, name: str = None):
        self.__name__ = name
        self.__es_expr__ = None
        self.__is_bool__ = False
        self.__value__ = None
        self.__has_set_value__ = None
        # self.is_equal = False

    def __neg__(self):
        ret = DocumentFields()
        ret.__es_expr__ = {
            "bool":
                {"must_not": self.__es_expr__}
        }
        return ret

    def contains(self, *args):
        ret = DocumentFields()
        values = args
        if isinstance(values, tuple):
            values = list(values)

        self.__is_bool__ = True
        # es_object = __make_up_es__(self.__name__, other)
        ret.__es_expr__ = {
            "terms": {
                self.__name__: values
            }
        }
        return ret

    def __getattr__(self, item):
        if item.lower() == "id":
            item = "_id"
        if self.__name__ is not None:
            return DocumentFields(f"{self.__name__}.{item}")
        return DocumentFields(item)

    def __eq__(self, other):
        ret = DocumentFields()
        self.__is_bool__ = True
        # es_object = __make_up_es__(self.__name__, other)
        ret.__es_expr__ = __make_up_es_syntax__(self.__name__, other)
        return ret

    def __or__(self, other):
        ret = DocumentFields()
        if isinstance(other, DocumentFields):
            if self.__is_bool__:
                left = {"bool": self.__es_expr__}
            else:
                left = self.__es_expr__
            if other.__is_bool__:
                rigt = {"bool": other.__es_expr__}
            else:
                rigt = other.__es_expr__

            ret.__es_expr__ = {
                "should": [
                    left, rigt
                ]
            }
            ret.__is_bool__ = True
            return ret
        else:
            raise Exception("invalid expr")

    def __and__(self, other):
        ret = DocumentFields()
        if isinstance(other, DocumentFields):
            if self.__is_bool__:
                left = {"bool": self.__es_expr__}
            else:
                left = self.__es_expr__
            if other.__is_bool__:
                rigt = {"bool": other.__es_expr__}
            else:
                rigt = other.__es_expr__
            # if rigt.get("match"):
            #     rigt["term"] = rigt["match"]
            #     del rigt["match"]
            ret.__es_expr__ = {
                "must": [
                    left, rigt
                ]
            }
            ret.__is_bool__ = True
            return ret

        else:
            raise Exception("invalid expr")

    def boost(self, value: float):
        if isinstance(self.__es_expr__, dict):
            self.__es_expr__["boost"] = value
        return self

    def __lshift__(self, other):
        if self.__name__ is None:
            raise Exception("Thous can not update expression")
        if other is not None:
            if type(other) not in [str, int, float, bool, datetime.datetime,dict,list]:
                raise Exception(
                    f"Thous can not update by non primitive type. {type(other)} is not in [str,str,int,float,bool,datetime.datetime,dict,list]")
        ret = DocumentFields(self.__name__)
        ret.__value__ = other
        ret.__has_set_value__ = True
        return ret

    def __repr__(self):
        if isinstance(self.__es_expr__, dict):
            return json.dumps(self.__get_expr__(), indent=1)
        return self.__name__

    def __get_expr__(self):
        if isinstance(self.__es_expr__, dict):
            ret = self.__es_expr__
            if self.__name__ is not None:
                return {
                    "term": {
                        self.__name__: {
                            "value": self.__es_expr__
                        }
                    }
                }
            if self.__is_bool__:
                ret = {
                    "bool": ret
                }
            return dict(query=ret)
        return self.__name__


"""
match_phraseBody = {
                "match_phrase": {
                    "content": {
                        "query": str_content,
                        "slop": 3,
                        "analyzer": "standard",
                        "zero_terms_query": "none",
                        "boost": 4.5
                    }
                }
            }
"""


def match(field: DocumentFields, content: str, boost: float = None):
    """

    :return:
    """
    ret = DocumentFields()
    __match_content__ = {
        "match": {
            field.__name__: {
                "query": content
                # "boost": 0.5

            }
        }
    }

    if boost is not None:
        __match_content__["boost"] = boost

    ret.__es_expr__ = __match_content__
    return ret


def match_phrase(field: DocumentFields, content: str, boost: float = None, slop=None,
                 analyzer="standard") -> DocumentFields:
    ret = DocumentFields()
    __match_phrase__ = {
        field.__name__: {
            "query": content,
            "analyzer": analyzer,
            "zero_terms_query": "none"
        }
    }
    if boost is not None:
        __match_phrase__["boost"] = boost
    if slop is not None:
        __match_phrase__["slop"] = slop
    ret.__es_expr__ = {
        "match_phrase": __match_phrase__
    }
    return ret


__cach__index__ = {}


def get_map(cls: type):
    ret = {}
    for k, v in cls.__annotations__.items():
        if v == str:
            ret[k] = "text"
        elif v == bool:
            ret[k] = "boolean"
        elif v == int:
            ret[k] = "long"
        elif v == float:
            ret[k] = "double"
        else:
            ret[k] = {"type": "nested"}
    return dict(
        mappings=dict(
            properties=ret
        )
    )


class SearchResultHits(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    @property
    def total(self) -> int:
        return self.get('total').get('value') or 0

    @property
    def hits(self) -> typing.List[dict]:
        return self.get('hits') or []

    @property
    def max_score(self) -> float:
        return self.get('max_score') or 0


class SearchResult(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    @property
    def hits(self) -> SearchResultHits:
        return SearchResultHits(self.get('hits') or {'value': 0})

    @property
    def took(self) -> int:
        return self.get('took') or 0

    @property
    def items(self):
        for x in self.hits.hits:
            yield ESDocumentObject(x)


def search(client: Elasticsearch,
           index: str,
           filter,
           excludes: typing.List[DocumentFields] = [],
           skip: int = 0,
           limit: int = 50,
           highlight: DocumentFields = None) -> SearchResult:
    if isinstance(filter, dict):
        body = dict(query=filter)

    elif isinstance(filter, DocumentFields):
        body = filter.__get_expr__()
    body["from"] = skip * limit
    body["size"] = limit
    if excludes.__len__() > 0:
        body["_source"] = {
            "excludes": [x.__name__ for x in excludes]
        }
    """
    __highlight = {
                "pre_tags": ["<em>"],
                "post_tags": ["</em>"],
                "fields": {
                    "content": {}
                }
            }
    """
    if highlight:
        __highlight = {
            "pre_tags": ["<em>"],
            "post_tags": ["</em>"],
            "fields": {
                highlight.__name__: {}
            }
        }
        body["highlight"] = __highlight
    ret = client.search(index=index, doc_type="_doc", body=body)
    return SearchResult(ret)


docs = DocumentFields()


def is_index_exist(client: Elasticsearch, index: str):
    return client.indices.exists(index)


class ESDocumentObject(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def get(self, key):

        if isinstance(key, DocumentFields):
            items = key.__name__split('.')
            ret = self
            for x in items:
                ret = dict.get(ret, x)
                if isinstance(ret, dict):
                    ret = ESDocumentObject(ret)
                if ret is None:
                    return None

            return ret
        else:
            return dict.get(self, key)

    def __getattr__(self, item):
        if isinstance(item, str) and item.lower() == "id":
            item = "_id"
        ret_val = self.get(item)
        if isinstance(ret_val, dict):
            return ESDocumentObject(**self.get(item))
        else:
            return ret_val

    def __setattr__(self, key, value):
        if isinstance(key, str) and key.lower() == "id":
            key = "_id"
        if isinstance(value, dict):
            dict.update(self, {key: ESDocumentObject(value)})

        else:
            dict.update(self, {key: value})

    def to_pydantic(self) -> pydantic.BaseModel:
        return pydantic.BaseModel(self)


class ESDocumentObjectInfo:
    """
    {'_index': 'long-test-2011-11',
 '_type': '_doc',
 '_id': '56330233-59f2-48b9-b213-72e75f9f9b28',
 '_version': 4,
 '_seq_no': 3,
 '_primary_term': 1,
 'found': True,
 '_source': {'user_name': 'root',
  'password': 'tes',
  'tags': ['a', 'b', 'c', 'd']}}
    """

    def __init__(self, data):
        """

        :param data:
        """
        self.__data__ = data

    @property
    def __index__(self) -> str:
        return self.__data__["_index"]

    @property
    def id(self) -> str:
        return self.__data__["_id"]

    @property
    def doc_type(self) -> str:
        return self.__data__["_type"]

    @property
    def source(self) -> ESDocumentObject:
        return ESDocumentObject(self.__data__["_source"])


def get_doc(client: Elasticsearch, index: str, id: str, doc_type: str = "_doc") -> ESDocumentObjectInfo:
    try:
        ret = client.get(index=index, id=id, doc_type=doc_type)
        return ESDocumentObjectInfo(data=ret)
    except elasticsearch.exceptions.NotFoundError as e:
        return None


def create_doc(client: Elasticsearch, index: str, body, id: str = None, doc_type: str = "_doc"):
    id = id or str(uuid.uuid4())

    res = client.create(index=index, doc_type=doc_type, id=id, body=body)
    res["_source"] = body

    return ESDocumentObjectInfo(res)


def update_doc_by_id(client: Elasticsearch, index: str, id: str, data, doc_type: str = "_doc"):
    data_update = data
    if isinstance(data, DocumentFields):
        if data.__has_set_value__ is None:
            raise Exception(
                f"Hey!\n what the fu**king that?\n.thous should call {data.__name__} << {{your value}} ")
        data_update = {
            data.__name__: data.__value__
        }
    elif isinstance(data, tuple):
        data_update = {}

        for x in data:
            if isinstance(x, DocumentFields):
                if x.__has_set_value__ is None:
                    raise Exception(
                        f"Hey!\n what the fu**king that?\n.thous should call {x.__name__} << {{your value}} ")
                data_update[x.__name__] = x.__value__
    try:
        client.update(
            index=index,
            id=id,
            doc_type=doc_type,
            body=dict(
                doc=data_update
            )

        )
        return data_update
    except elasticsearch.exceptions.NotFoundError as e:
        return None


def create_index(client: Elasticsearch, index: str, body: typing.Union[dict, type]):
    if inspect.isclass(body) and body not in [str, datetime.datetime, int, bool, float, int]:
        ret = client.indices.create(index=index, body=get_map(body))
    else:
        ret = client.indices.create(index=index, body=body)
    return ret


def delete_doc(client: Elasticsearch, index: str, id: str, doc_type: str = "_doc"):
    try:
        ret = client.delete(index=index, id=id, doc_type=doc_type)
        return ret
    except elasticsearch.exceptions.NotFoundError as e:
        return None


from enum import Enum


class __expr_type_enum__(Enum):
    CALL = 1
    """
    Function call
    """
    OPER = 2
    """
    Operand
    """
    LOGI = 3


__map__ = {
    "$and": dict(name="__and__", _type=__expr_type_enum__.LOGI),
    "$or": dict(name="__or__", _type=__expr_type_enum__.LOGI),
    "$contains": dict(name="contains", _type=__expr_type_enum__.CALL),
    "$not": dict(name="__neg__", _type=__expr_type_enum__.OPER)
}


def __all_primitive__(x):
    if type(x) in [str, int, float, bool, datetime.datetime]:
        return True
    elif isinstance(x, list):
        for v in x:
            if not __all_primitive__(v):
                return False
        return True


def create_filter_from_dict(expr: dict, owner_caller=None):
    global __map__
    if isinstance(expr, dict):

        for k, v in expr.items():
            if k[0:1] == "$":
                if not __map__.get(k):
                    raise Exception(f"{k} is Unknown")
                if __map__.get(k):
                    map_name = __map__[k]["name"]
                    map_type: __expr_type_enum__ = __map__[k]["_type"]

                    if isinstance(v, list):
                        if __all_primitive__(v) and map_type == __expr_type_enum__.CALL:
                            ret = getattr(owner_caller, map_name)(*v)
                            return ret
                        else:
                            ret = create_filter_from_dict(v[0])
                            if v.__len__() > 1:
                                for i in range(1, v.__len__()):
                                    next = create_filter_from_dict(v[i])
                                    if map_type == __expr_type_enum__.LOGI:
                                        ret = getattr(ret, map_name)(next)
                                    else:
                                        # if owner_caller is not None:
                                        #     ret = getattr(owner_caller, method_name)(next)
                                        # else:
                                        raise NotImplemented
                            return ret
                    else:
                        if map_type == __expr_type_enum__.OPER:
                            ret = create_filter_from_dict(v)
                            ret = getattr(ret, map_name)()
                            return ret
                        else:
                            raise NotImplemented
            else:
                if isinstance(v, dict):
                    ret = DocumentFields(k)
                    ret = create_filter_from_dict(v, ret)
                    return ret
                else:
                    ret = DocumentFields(k)
                    ret = ret == v
                    return ret



    else:
        raise NotImplemented
