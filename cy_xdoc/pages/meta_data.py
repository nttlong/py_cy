import cy_web
def get_meta_data():
    return dict(
        version="1",
        full_url_app=cy_web.get_host_url(),
        full_url_root=cy_web.get_host_url(),
        api_url=cy_web.get_host_url()+"/api",
        host_dir=cy_web.get_host_dir()
    )