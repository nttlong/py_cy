import os.path
import pathlib

import cy_kit

__working_foler__ = pathlib.Path(__file__).parent.parent.__str__()
__yaml_path__ =os.path.join(__working_foler__,"config.yml")
class DbContext:
    def __init__(self,config=cy_kit.yaml_config(__yaml_path__)):
        self.host =config.db.host
        self.port = config.db.port
        print(f"connect to {self.host}:{self.port}")
