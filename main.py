import os
from .download_handler import download_url
from .csv_handler import convert_csv_to_xlsx
from .handler import set_env
from .MS_GRAPH import send_mail
from .MS_GRAPH import get_access_token
from .MS_GRAPH.drive_handler import upload_to_onedrive

from .settings import settings


def main() :
    try :
        #load env variables
        set_env()
        #load access token into environment 
        get_access_token()

        if not os.path.exists(os.environ["APPLICATION_PATH"]) :
            os.mkdir(os.environ["APPLICATION_PATH"])

        url = input("enter download URL... ")

        #download the file
        download_response = download_url(url)

        if download_response["status_code"] == -1 :
            print("download failed...")
            print("Program exitting")
            exit()

        #convert csv to xlsx format
        convert_response = convert_csv_to_xlsx(download_response["file_path"])

        documents = [
            {
                "file_path" : convert_response["file_path"],
                "file_name" : "Converted_Qualys_Daily_Report.xlsx"
            }
        ]

        #send mail to respective recipients
        mail_response = send_mail(
            subject="Qualys Daily Report",
            content= """Hi team,here im attaching cleaned version of Qualys Daily Report  """,
            toRecipients=settings["toRecipients"],
            ccRecipients=settings["ccRecipients"],
            attachments=documents
        )
        print(mail_response["message"])

        
        #upload to Onedrive
        for file in documents :
            response = upload_to_onedrive(file_info=file,parent_id=settings["drive_folder_id"])
            if response["status_code"] == 201 :
                print(f"{file['file_path']} file uploaded")


    except Exception as e :

        print("Error raised",e)
        exit
    








if __name__ == "__main__" :
    main()
    
