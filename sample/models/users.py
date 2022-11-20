import cy_docs
@cy_docs.define(
    name="users",
    uniques=["useraname","email"],
    indexes=["tanent"]
)
class Users:
    Username:str