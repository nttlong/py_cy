import cy_kit
import cy_web
from cy_xdoc.auths import Authenticate
import fastapi.params
from cy_xdoc.services.apps import AppServices
from cy_xdoc.controllers.models.apps import AppInfo, AppInfoRegister, AppInfoRegisterResult
import cy_xdoc

@cy_web.hanlder(method="post", path="{app_name}/apps/register")
def get_list_of_apps(app_name: str, Data: AppInfoRegister,
                     token=fastapi.Depends(Authenticate)) -> AppInfoRegisterResult:
    data = Data.dict()
    del data["AppId"]
    app = cy_xdoc.container.service_app.create(**data)
    ret = AppInfoRegisterResult()
    ret.Data = app.to_pydantic()
    return ret
