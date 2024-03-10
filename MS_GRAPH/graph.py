import os
import webbrowser
import requests
from msal import PublicClientApplication,ConfidentialClientApplication
from .helper import load_pickle,create_pickle,verify_token,PICKLE_PATH
from .settings import settings


CLIENT_ID = settings["CLIENT_ID"]

CLIENT_SECRET = settings["CLIENT_SECRET"]

SCOPES = settings["SCOPES"]

def get_authorization_code() :

    client = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET
    )

    authorize_url = client.get_authorization_request_url(SCOPES)

    webbrowser.open(url=authorize_url,new=True)

    code_url = input("Please got to browser and authorize tyen copy the url send back to here ")

    code = code_url.split("?")[-1].split("&")[0][5:]

    return code




def get_access_token(code="") :

    if not os.path.exists(PICKLE_PATH) :

        if not code :
            code = get_authorization_code() 

        API_ENDPOINT = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

        payload = {
            "client_id" : CLIENT_ID,
            "client_secret" : CLIENT_SECRET,
            "grant_type" : "authorization_code",
            "code" : code,
            "scope" : "user.read"
        }
        headers = {"Content-Type" : "application/x-www-form-urlencoded"}

        response = requests.post(url=API_ENDPOINT,data=payload,headers=headers)

        if response.status_code == 200 :
            create_pickle(response)
            load_pickle()

            return response.json()["access_token"]
        else :
            print(response.content)
    else :

        load_pickle()

        if not verify_token() :
            renew_access_token(os.environ["REFRESH_TOKEN"])

    


def renew_access_token(refresh_token="") :

    API_ENDPOINT = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    payload = {
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
        "grant_type" : "refresh_token",
        "refresh_token" : refresh_token,
        "scope" : "user.read"
    }
    headers = {"Content-Type" : "application/x-www-form-urlencoded"}

    response = requests.post(url=API_ENDPOINT,data=payload,headers=headers)

    create_pickle(response)

    load_pickle()








    

    