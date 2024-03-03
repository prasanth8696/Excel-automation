import os
import json


def set_env() :

    with open("env.json","r") as file :

        env_data = json.load(file)

        print(env_data)

        for variable,value in env_data.items() :

            os.environ[variable] = eval(value)

    
