# Contains all the generic code

import yaml
from networksecurity.exception.exception import NetworkSecurtiyException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
# import dill
import pickle

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            # yaml.safe_load() safely loads YAML (avoids executing arbitrary code)
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurtiyException(e,sys)

def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurtiyException(e,sys)