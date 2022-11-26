
import fastapi
import cy_web
import cy_kit
import cy_xdoc.auths
from cy_xdoc.services.files import FileServices
from cy_xdoc.controllers.models.files_register import RegisterUploadInfo,RegisterUploadInfoResult
@cy_web.hanlder("post","{app_name}/files/register")
async def register_new_upload(app_name: str, Data: RegisterUploadInfo,token = fastapi.Depends(cy_xdoc.auths.Authenticate))->RegisterUploadInfoResult:
    """

    :param app_name: Ứng dụng nào cần đăng ký Upload
    :param Data: Thông tin đăng ký Upload
    :param token:
    :return:
    """
    file_service = cy_kit.single(FileServices)

    ret = file_service.add_new_upload_info(
        app_name=app_name,
        chunk_size= Data.ChunkSizeInKB * 1024,
        file_size= Data.FileSize,
        client_file_name= Data.FileName,
        is_public= Data.IsPublic,
        thumbs_support= Data.ThumbConstraints,
        web_host_root_url= cy_web.get_host_url(),
        privileges_type= Data.Privileges

    )
    return RegisterUploadInfoResult(Data = ret.to_pydantic())



