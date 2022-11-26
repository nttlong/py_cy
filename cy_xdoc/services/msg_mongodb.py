import datetime
import uuid
from _testcapi import matmulType

import cy_docs
import cy_kit
from cy_xdoc.services.msg import MessageService
from cy_xdoc.services.base import Base
from cy_xdoc.models.files import SysMessage
import pathlib
import os
import re


@cy_kit.must_imlement(MessageService)
class MessageServiceMongodb(Base):
    def __init__(self):
        self.instance_id = str(uuid.uuid4())
        self.working_dir = pathlib.Path(__file__).parent.parent.parent.__str__()
        self.lock_dir = os.path.join(self.working_dir, "background_service_files", "msg_lock")
        if not os.path.isdir(self.lock_dir):
            os.makedirs(self.lock_dir, exist_ok=True)
        files = list(list(os.walk(self.lock_dir))[0][2])
        val_id = None
        UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
        for x in files:
            file_name = pathlib.Path(x).stem
            if UUID_PATTERN.match(file_name):
                val_id = file_name
                break
        if val_id is None:
            with open(os.path.join(self.lock_dir, self.instance_id), 'wb') as f:
                f.write(self.instance_id.encode('utf8'))
        else:
            self.instance_id = val_id

    def emit(self, app_name: str, message_type: str, data: dict):
        doc = cy_docs.expr(SysMessage)
        self.db('admin').doc(SysMessage).insert_one(
            doc.Data << data,
            doc.MsgId << str(uuid.uuid4()),
            doc.AppName << app_name,
            doc.MsgType << message_type,
            doc.CreatedOn << datetime.datetime.utcnow(),
            doc.IsLock << False,
            doc.InstancesLock << {
                self.instance_id: True
            }
        )
