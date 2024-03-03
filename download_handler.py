import os
import requests


def download_url(url:str)-> dict :

    try :
        
        if not os.path.exists(os.environ["DOWNLOAD_PATH"]) :
            os.mkdir(os.environ["DOWNLOAD_PATH"])
        
        response = requests.get(url=url,stream=True)

        #response.raise_for_status()

        #Get Filename from headers
        file_path = os.path.join(os.environ["DOWNLOAD_PATH"],response.headers["Content-Disposition"].split("filename=")[-1])

        with open(file_path,"wb") as file :
            #data_downloaded = 0
            print(f"File Downloading {os.path.basename(file_path)}")
            for chunk in response.iter_content(chunk_size=8192) :
                file.write(chunk)
                
                #data_downloaded += 8192
                #print("{}MB file downloaded ".format(data_downloaded/1024))

        print(f"{os.path.basename(file_path)} downloaded successfully")

        return {"status_code" : 0,"file_path" : file_path}



    except Exception  as e:
        print( "Something went wrong",e)

        return {"status_code" : -1,"file_path" : ""}

