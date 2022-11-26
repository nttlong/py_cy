import fastapi
import typing

import cy_docs
import cy_kit
import cy_web
import cy_xdoc.auths
import cy_xdoc.models.files
import cy_xdoc.controllers.models.files_register
import cy_xdoc.services.files


@cy_web.model()
class DataPrivileges:
    UploadId: str
    Privileges: typing.List[cy_xdoc.controllers.models.files_register.PrivilegesType]


@cy_web.model()
class Err:
    message: str


@cy_web.model()
class Result:
    is_ok: bool
    error: typing.Optional[Err]


@cy_web.hanlder(method="post", path="{app_name}/files/add_privileges")
def add_privileges(
        app_name: str,
        Data: typing.List[cy_xdoc.controllers.models.files_register.PrivilegesType],
        UploadIds: typing.List[str],
        token=fastapi.Depends(cy_xdoc.auths.Authenticate)) -> Result:
    file_services = cy_kit.singleton(cy_xdoc.services.files.FileServices)
    for upload_id in UploadIds:
        ret = file_services.add_privileges(
            app_name=app_name,
            upload_id=upload_id,
            privileges=[cy_docs.DocumentObject(x) for x in Data]

        )
    return Result(is_ok=True)
