import os.path
import pathlib

import cy_kit
config = cy_kit.yaml_config(os.path.join(
    pathlib.Path(__file__).parent.parent.parent.__str__(),"config.yml"
))
config_path = os.path.join(pathlib.Path(__file__).parent.parent.parent.__str__(),"config.yml")
if  config.message_when_upload == False:
    print(f"Warning! disable all media content process\n\tPlease open file {config_path}\n\tset message_when_upload is true")