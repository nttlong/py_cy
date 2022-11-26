import typing
import cy_web
@cy_web.model()
class ErrorResult:
    Code:str
    Message:str
    Fields: typing.List[str]