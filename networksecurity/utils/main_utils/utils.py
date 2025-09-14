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