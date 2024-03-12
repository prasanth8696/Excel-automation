import os
import requests


def check_file_size(file_info) :

    if not os.path.exists(file_info["file_path"]) :
        print(f"{file_info["file_path"]} not exists")
        return 
    size = os.path.getsize(file_info["file_path"]) / (1024 * 1024)  #convert bytes to megabytes

    return size

#if File size is more than 200MB this function will trigger to chunk upload 
def upload_large_file(upload_session_url="",file_info={}) :
    pass



#upload files in Drive
def upload_to_onedrive(drive="me",parent_id="root",file_info={}) :
   
    API_ENDPOINT = f"https://graph.microsoft.com/v1.0/me/drive/items/{parent_id}:/{file_info["file_name"]}:/content"

    
    headers = {
                    "Authorization" : "Bearer " + os.environ["ACCESS_TOKEN"]
    }
    
    if check_file_size(file_info) > 200 :
        pass
    else:

        #Read the file
        with open(file_info["file_path"],"rb") as upload :
            upload_content = upload.read()

        #upload a small file to onedrive
        try :
            response = requests.put(url=API_ENDPOINT,headers=headers,data=upload_content)

            return {"status_code" : response.status_code,"message" : response.json()}

        except Exception as e :
            return {"status_code" : response.status_code,"message" : response.json()
            }
