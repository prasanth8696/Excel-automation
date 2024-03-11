import os
import json
from .settings import settings



def set_env() :

    with open(settings["env_path"],"r") as file :

        env_data = json.load(file)

        print(env_data)

        for variable,value in env_data.items() :

            os.environ[variable] = eval(value)

    
