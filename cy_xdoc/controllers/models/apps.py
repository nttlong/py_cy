import typing
import cy_web
from cy_xdoc.controllers.models.errors import ErrorResult
@cy_web.model()
class AppInfo:
    """
    Infomation of application, an application is one-one mapping to tanent
    """
    AppId:typing.Optional[str]
    """
    The __name__ of application
    """
    Name:str
    Description: typing.Optional[str]
    Domain: typing.Optional[str]
    LoginUrl:typing.Optional[str]
    ReturnUrlAfterSignIn:typing.Optional[str]
from pydantic import Field
def warpper():
    return
@cy_web.model()
class AppInfoRegister(AppInfo):
    # """
    #     Infomation of application, an application is one-one mapping to tanent
    #     """
    # AppId: str
    # """
    # The __name__ of application
    # """
    # Name: str
    # Description: typing.Optional[str]
    # Domain: typing.Optional[str]
    # LoginUrl: typing.Optional[str]
    # ReturnUrlAfterSignIn: typing.Optional[str]

    UserName:typing.Optional[str]
    """
    Co cung dc kg co cung khong sao
    """
    Password:typing.Optional[str]
@cy_web.model()
class AppInfoRegisterResult:
    Data:typing.Optional[AppInfo]
    Error:typing.Optional[ErrorResult]

