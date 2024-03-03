import os
from download_handler import download_url
from csv_handler import convert_csv_to_xlsx
from handler import set_env


def main() :
    try :
        #load env variables
        set_env()

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
        
        #upload to Onedrive


    except Exception as e :

        print("Error raised",e)
        exit
    








if __name__ == "__main__" :
    main()
    
