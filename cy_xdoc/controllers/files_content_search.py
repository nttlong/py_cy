import fastapi
import cy_xdoc.services.search_engine
import cy_kit
import cy_web
import cy_xdoc.auths
from typing import Optional
@cy_web.hanlder("post","{app_name}/search")
def file_search(app_name: str, content: str,
                      page_size: Optional[int],
                      page_index: Optional[int],
                      highlight: Optional[bool],
                      token = fastapi.Depends(cy_xdoc.auths.Authenticate)):
    """
    Tim kiem noi dung
    :param request:
    :param app_name:
    :param content:
    :param page_size:
    :param page_index:
    :param token:
    :return:
    """
    if highlight is None:
        highlight=False
    search_services:cy_xdoc.services.search_engine.SearchEngine = cy_kit.singleton(cy_xdoc.services.search_engine.SearchEngine)
    # search_result = search_content_of_file(app_name, content, page_size, page_index)
    search_result=search_services.full_text_search(
        app_name=app_name,
        content =content,
        page_size=page_size,
        page_index=page_index,
        highlight=highlight
    )

    ret_items = []
    url = cy_web.get_host_url()+"/api"
    for x in search_result.items:
        upload_doc_item = x._source.data_item
        if upload_doc_item:
            # upload_doc_item.UploadId = upload_doc_item._id
            upload_doc_item.Highlight = x.highlight
            upload_doc_item.UrlOfServerPath= f"{url}/{app_name}/file/{upload_doc_item.FullFileName}"
            upload_doc_item.AppName = app_name
            upload_doc_item.RelUrlOfServerPath = f"/{app_name}/file/{upload_doc_item.FullFileName}"
            upload_doc_item.ThumbUrl = url + f"/{app_name}/thumb/{upload_doc_item['_id']}/{upload_doc_item.FileName}.png"
            ret_items += [upload_doc_item]

    return dict(
        total_items=search_result.hits.total,
        max_score=search_result.hits.max_score,
        items=ret_items,
        text_search=content
    )
