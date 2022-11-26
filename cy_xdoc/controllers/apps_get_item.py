import cy_kit
import cy_web
from cy_xdoc.auths import Authenticate
import fastapi.params
from cy_xdoc.services.apps import AppServices
from cy_xdoc.controllers.models.apps import AppInfo


@cy_web.hanlder(method="post", path="{app_name}/apps/get/{get_app_name}")
def get_list_of_apps(app_name: str, get_app_name: str, token=fastapi.Depends(Authenticate)) -> AppInfo:
    app_service = cy_kit.single(AppServices)
    return app_service.get_item(app_name, app_get=get_app_name).to_pydantic()
