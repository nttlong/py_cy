"""
Hiển thị nội dung OCR của file ảnh
"""
import fastapi
import cy_xdoc.auths
import cy_web
import cy_xdoc
import mimetypes
import cy_kit
import cy_xdoc.services.files
import cy_xdoc.services.file_storage
@cy_web.hanlder("get","{app_name}/file-ocr/{directory:path}")
def files_contet_orc(app_name: str, directory: str, request: fastapi.Request,
                        token: str =fastapi.Depends(cy_xdoc.auths.Authenticate)):
    """
    Xem hoặc tải nội dung file
    :param app_name:
    :return:
    """
    import asyncio
    mime_type, _ = mimetypes.guess_type(directory)

    file_service:cy_xdoc.services.files.FileServices = cy_kit.singleton(cy_xdoc.services.files.FileServices)
    file_store_service = cy_kit.singleton(cy_xdoc.services.file_storage.FileStorageService)
    upload_id = directory.split('/')[0]
    upload = file_service.get_upload_register(app_name=app_name,upload_id=upload_id)
    if upload is None:
        return fastapi.Response(status_code=401)
    if upload.get("OCRFileId") is None:
        return fastapi.Response(status_code=401)
    fs = file_store_service.get_file_by_id(
        app_name=app_name,
        id=upload.OCRFileId

    )

    if fs is None:
        return fastapi.Response(status_code=401)
    mime_type, _ = mimetypes.guess_type(directory)
    ret = asyncio.run(cy_web.cy_web_x.streaming_async(fs, request, mime_type))
    return ret

