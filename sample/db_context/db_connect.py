import pymongo

import cy_kit
class DbConnect:
    def __init__(self,config=cy_kit.yaml_config("./config.yml")):
        self.client= pymongo.MongoClient(**config.mongodb)
        print("Connect to mongo database")
