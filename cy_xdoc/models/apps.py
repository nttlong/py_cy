from datetime import datetime
import cy_docs
from bson import ObjectId
@cy_docs.define(
    name="sys_applications",
    uniques=["Name","NameLower","Email"],
    indexes=["Domain","LoginUrl","ReturnUrlAfterSignIn"]
)
class App:
    import bson
    _id:str
    Name:str
    NameLower:str
    """
    Để cho truy cập nhanh dùng NameLower so sánh với giá trị lower
    """
    RegisteredBy:str
    RegisteredOn:datetime
    ModifiedOn:datetime
    Domain:str
    LoginUrl:str
    SecretKey:str
    ReturnUrlAfterSignIn:str
    Description:str
    Email:str
    Username:str
    Password:str
    SecretKey:str
    """
    Email dùng để liên lạc với application khi cần. Ví dụ dùng trong trường ho75ptruy tìm lại mật khẩu của user root trên app
    """

