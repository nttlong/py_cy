import logging
import pathlib
import os
import cy_kit
class Config:
    def __init__(self):
        self.working_folder = pathlib.Path(__file__).parent.parent.__str__()


    def load(self, yaml_config_path):
        self.config_path = yaml_config_path
        if self.config_path[0:2] == "./":
            self.config_path = os.path.abspath(os.path.join(
                self.working_folder,
                self.config_path[2:].replace('/', os.sep)
            ))
        self.config_data = cy_kit.yaml_config(self.config_path)

    def __getattr__(self, item):
        return getattr(self.config_data,item)

class Base:
    def __init__(
            self,
            config:Config=cy_kit.singleton(Config)):
        self.config=config
        self.working_folder = config.working_folder
        self.host_ip=cy_kit.get_local_host_ip()
        self.logs: logging.Logger=None


    def init(self, name):
        self.logs = cy_kit.create_logs(
           os.path.join(self.working_folder,"logs"),name)
        self.processing_folder = self.config.tmp_media_processing_folder
        if self.processing_folder[0:2] == "./":
            self.processing_folder = self.processing_folder[2:]
            self.processing_folder = os.path.abspath(
                os.path.join(self.working_folder, self.processing_folder.replace('/', os.sep)))
        self.processing_folder = os.path.join(self.processing_folder, name)
        self.processing_folder = self.processing_folder.replace('/', os.sep)
        if not os.path.isdir(self.processing_folder):
            os.makedirs(self.processing_folder, exist_ok=True)

    def get_file_extenstion(self, file_path)->str:
        return os.path.splitext(file_path)[1][1:]
    def get_file_name_only(self,file_path)->str:
        return pathlib.Path(file_path).stem

