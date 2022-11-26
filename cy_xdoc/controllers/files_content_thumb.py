import os.path
import cy_kit
import cy_web
from fastapi import Request,Response
from fastapi.responses import FileResponse
from cy_xdoc.services.files import FileServices
import mimetypes
import cy_xdoc
@cy_web.hanlder("get","{app_name}/thumb/{directory:path}")
async def get_thumb_of_files(app_name: str, directory: str, request: Request):
    """
    Xem hoặc tải nội dung file
    :param app_name:
    :return:
    """
    thumb_dir_cache = os.path.join(app_name,"thumbs")
    cache_thumb_path = cy_web.cache_content_check( thumb_dir_cache,directory.lower().replace("/","_"))
    if cache_thumb_path:
        return FileResponse(cache_thumb_path)

    upload_id = directory.split('/')[0]
    fs = cy_xdoc.container.service_file.get_main_main_thumb_file(app_name,upload_id)
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

