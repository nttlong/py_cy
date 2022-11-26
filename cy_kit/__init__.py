import os.path
import pathlib
import sys
from typing import TypeVar

__working_dir__ = pathlib.Path(__file__).parent.__str__()

import cy_kit

sys.path.append(__working_dir__)

import cy_kit_x

container = cy_kit_x.container

T = TypeVar('T')


def single(cls: T) -> T:
    return cy_kit_x.resolve_singleton(cls)


def instance(cls: T) -> T:
    return cy_kit_x.resolve_scope(cls)


def config_provider(from_class: type, implement_class: type):
    cy_kit_x.config_provider(from_class, implement_class)

from typing import Generic

# class Provider(Generic[T]):
#     def __init__(self,__cls__:type):
#         self.__cls__=__cls__
#         self.__ins__ =None
#     @property
#     def instance(self)->T:
#         if self.__ins__  is None:
#             self.__ins__ = cy_kit_x.provider(self.__cls__)
#         return self.__ins__




def provider(cls: T) -> T:
    return cy_kit_x.provider(cls)


def check_implement(from_class: type, implement_class: T) -> T:
    cy_kit_x.check_implement(from_class, implement_class)
    return implement_class


def must_imlement(interface_class: type):
    return cy_kit_x.must_implement(interface_class)


def yaml_config(path: str, apply_sys_args: bool = True):
    return getattr(cy_kit_x, "yaml_config")(path, apply_sys_args)


def combine_agruments(data):
    return getattr(cy_kit_x, "combine_agruments")(data)


def inject(cls:T)->T:
    return cy_kit_x.inject(cls)
def singleton(cls:T)->T:
    return cy_kit_x.singleton(cls)
def scope(cls:T)->T:
    return cy_kit_x.scope(cls)


def thread_makeup():
    return cy_kit_x.thread_makeup()
def get_local_host_ip():
    return cy_kit_x.get_local_host_ip()


def create_logs(log_dir, name):
    return cy_kit_x.create_logs(log_dir,name)


def get_runtime_type(injector_instance):
    return cy_kit_x.get_runtime_type(injector_instance)


def singleton_from_path(injector_path:str):
    """

    :param injector_path: <module>:<class name>
    :return:
    """
    return cy_kit_x.singleton_from_path(injector_path)