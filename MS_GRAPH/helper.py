import os
import pickle
import requests
from settings import settings






#PICKLE_PATH = os.path.join(os.getcwd(),settings["PICKLE_NAME"])
PICKLE_PATH = "C:\VM_AUTOMATION\MS_GRAPH\MS-GRAPH-token.pickle"


def create_pickle(response,file_path=PICKLE_PATH) :

    with open(file_path,"wb") as file :

        pickle.dump(response,file)


def load_pickle(file_path=PICKLE_PATH) :

    #if pickle not there create a pickle file
    if not os.path.exists(file_path) :
        return
    
    with open(file_path,"rb") as file :
        response = pickle.load(file)

        #load values in env variables
        os.environ["ACCESS_TOKEN"] = response.json()["access_token"]
        os.environ["REFRESH_TOKEN"] = response.json()["refresh_token"]


def verify_token() :

    API_ENDPOINT = "https://graph.microsoft.com/v1.0/me"

    headers = {
                    "Authorization" : "Bearer " + os.environ["ACCESS_TOKEN"]
    }
    response = requests.get(url=API_ENDPOINT,headers=headers)

    if response.status_code == 200 :
        print(response.json())
        return True




def generate_scope() :

    current_scopes = settings["SCOPES"] 

    scopes_str = ""

    for scope in current_scopes :
        scopes_str += scope + " "

    return scopes_str