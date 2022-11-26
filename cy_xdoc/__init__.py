import fastapi
import cy_kit
import cy_xdoc.services.file_storage
import cy_xdoc.services.file_storage_mongodb

from cy_xdoc.services.apps import AppServices
from cy_xdoc.services.accounts import AccountService

import cy_xdoc.services.file_storage_disk
import cy_xdoc.services.files
import cy_xdoc.services.msg
import cy_xdoc.services.msg_mongodb

import cy_xdoc.services.search_engine
import cy_xdoc.services.files
import cy_xdoc.services.apps
import cy_xdoc.services.msg
import cy_xdoc.services.file_storage
import cy_xdoc.services.file_storage_mongodb
import cy_xdoc.services.file_storage_disk
import cy_xdoc.services.search_engine
import cy_xdoc.services.accounts
import cy_xdoc.services.secutities
import cy_xdoc.services.base

cy_kit.config_provider(
    from_class=cy_xdoc.services.file_storage.FileStorageService,
    implement_class=cy_xdoc.services.file_storage_mongodb.MongoDbFileService
)
# cy_kit.config_provider(
#     from_class=cy_xdoc.services.file_storage.FileStorageService,
#     implement_class=cy_xdoc.services.file_storage_disk.FileDiskStorageService
# )
"""
Cau hinh luu file dung mongodb
"""
cy_kit.config_provider(
    from_class=cy_xdoc.services.msg.MessageService,
    implement_class=cy_xdoc.services.msg_mongodb.MessageServiceMongodb
)
"""
Cau hinh he thong msg dung Mongodb
"""


class Container:
    def __init__(self,
                 data_context: cy_xdoc.services.base.DbConnect = cy_kit.singleton(cy_xdoc.services.base.DbConnect),
                 service_search: cy_xdoc.services.search_engine.SearchEngine = cy_kit.singleton(
                     cy_xdoc.services.search_engine.SearchEngine),
                 service_file: cy_xdoc.services.files.FileServices = cy_kit.singleton(
                     cy_xdoc.services.files.FileServices),
                 service_app: cy_xdoc.services.apps.AppServices = cy_kit.singleton(cy_xdoc.services.apps.AppServices),
                 services_msg: cy_xdoc.services.msg.MessageService = cy_kit.singleton(
                     cy_xdoc.services.msg.MessageService),
                 service_storage: cy_xdoc.services.file_storage.FileStorageService = cy_kit.singleton(
                     cy_xdoc.services.file_storage.FileStorageService),
                 service_account: cy_xdoc.services.accounts.AccountService = cy_kit.singleton(
                     cy_xdoc.services.accounts.AccountService),
                 service_sercutity: cy_xdoc.services.secutities.Sercurity = cy_kit.singleton(
                     cy_xdoc.services.secutities.Sercurity)

                 ):
        self.service_search = service_search
        self.service_file = service_file
        self.service_app = service_app
        self.services_msg = services_msg
        self.service_storage = service_storage
        self.service_account = service_account
        self.service_sercutity = service_sercutity
        self.data_context = data_context

container:Container = cy_kit.singleton(Container)
"""
Khoi tao container
"""