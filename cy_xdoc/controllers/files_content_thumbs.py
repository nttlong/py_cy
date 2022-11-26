import cy_kit, cy_web
import os
from fastapi import Response,Request
from fastapi.responses import FileResponse
import cy_xdoc.services.files
import cy_xdoc.services.file_storage
import mimetypes
@cy_web.hanlder(method="get",path="{app_name}/thumbs/{directory:path}")
async def get_thumb_of_files(app_name: str, directory: str,request:Request):
    """
    Xem hoặc tải nội dung file
    :param app_name:
    :return:
    """
    file_storage_service = cy_kit.singleton(cy_xdoc.services.file_storage.FileStorageService)
    thumb_dir_cache = os.path.join(app_name, "custom_thumbs")
    cache_thumb_path = cy_web.cache_content_check(thumb_dir_cache, directory.lower().replace("/", "_"))
    if cache_thumb_path:
        return FileResponse(cache_thumb_path)


    fs = file_storage_service.get_file_by_name(
        app_name=app_name,
        rel_file_path=f"thumbs/{directory}"
    )
    if fs is None:
        return Response(
            status_code=401
        )
    content = fs.read(fs.get_size())
    fs.seek(0)
    cy_web.cache_content(thumb_dir_cache, directory.replace('/', '_'), content)
    del content
    mime_type, _ = mimetypes.guess_type(directory)
    ret = await cy_web.cy_web_x.streaming_async(fs, request, mime_type)
    return ret




