import cy_kit
import cy_web
from cy_xdoc.auths import Authenticate
import fastapi.params
from typing import List
from cy_xdoc.services.apps import AppServices
from cy_xdoc.controllers.models.apps import AppInfo
@cy_web.hanlder(method="post", path="{app_name}/apps")
def get_list_of_apps(app_name:str,token = fastapi.Depends(Authenticate))->List[AppInfo]:
    app_service=cy_kit.single(AppServices)
    for app in  app_service.get_list(app_name):
        yield app.to_pydantic()

