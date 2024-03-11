import os
import base64
import requests



#generate recipients format
def generate_recipients(recipients=[])  :

    formatted_recipients_list = []

    for recipient in recipients :
        #Add all address in formatted way
        template = {
            "emailAddress" : {
                "address" : recipient,
            }
        }
        formatted_recipients_list.append(template)

    return formatted_recipients_list

def draft_attachments(attachments) :

    formatted_attachments_list = []

    for attachment in attachments :

        if os.path.exists(attachment["file_path"]) :

            with open(attachment["file_path"],"rb") as data :
                #Graph API will accept only base64 format
                media_content = base64.b64encode(data.read())

                attachment_template = {
                    "@odata.type" : "#microsoft.graph.fileAttachment",
                    "contentBytes" : media_content.decode("utf-8"),
                    "name" : attachment["name"]

                }
                formatted_attachments_list.append(attachment_template)

    return formatted_attachments_list

#download Attachments 
def download_attachments(mail_id,headers,save_dir=os.getcwd()) :
    try :
        API_ENDPOINT = f"https://graph.microsoft.com/v1.0/me/messages/{mail_id}/attachments"
        response = requests.get(url=API_ENDPOINT,headers=headers)

        attachments_list = response.json()["value"]["attachment"]

        attachments_path_list = []

        for attachment in attachments_list :
            attachment_name = attachment["name"]
            attachment_id = attachment["id"]

            API_ENDPOINT = f"https://graph.microsoft.com/v1.0/me/messages/{mail_id}/attachments/{attachment_id}/$value"

            MIME_content = requests.get(url=API_ENDPOINT,headers=headers)

            with open(os.path.join(save_dir,attachment_name),"wb") as file :
                file.write(MIME_content.content)
                attachments_path_list.append(save_dir,attachment_name)

        return attachments_path_list


    except Exception as e :
        print("exception raised",e)
        return False




#send mail
def send_mail(subject="",content="",toRecipients=[],ccRecipients=[],is_attachments=False,attachments=[],importance="normal",content_type="text",save_to_send_items=True) :

    """
        param: subject => what is the subject of the mail, DEFAULT => ""
        param: content => actual body of the mail, DEFAULT => ""
        param: content_type => which type of content you want to send two possible value "text" or "HTML", DEFAULT => "text"
        param: recipients => whom you need to send (to address), DEFAULT => []
        param: ccrecipients => cc address of the mail, DEFAULT => []
        param: is_attachments => if attachments need to send enable this param, DEFAULT => True
        param: attachements => list of attachment files path, DEFAULT =>[] or [{"file_path" : "","name" : ""}] 
        param: importance => priority of the mail, DEFAULT => normal
        param: save_to_send_items => if you want save mail into saveitems folder enable this param, DEFAULT => True
    """
    API_ENDPOINT = "https://graph.microsoft.com/v1.0/me/sendMail"

    if attachments :
        is_attachments = True

    headers = {
                    "Authorization" : "Bearer " + os.environ["ACCESS_TOKEN"],
                    "Content-Type" : "application/json"
    }

    request_body = {
        "message" : {
            "subject" : subject,

            "body" : {
                "contentType" : content_type,
                "content" : content
            },

            "toRecipients" : generate_recipients(toRecipients),

            "ccRecipients" : generate_recipients(ccRecipients),

            "importance" :importance
        }
    }
    #Add the attachments to request body
    if is_attachments :
        request_body["message"]["attachments"] = draft_attachments(attachments)


    #Add saveToSendItems if save_to_send_items is false
    if not save_to_send_items :
        request_body["saveToSentItems"] = False

    #make a requests to graph API
    response = requests.post(url=API_ENDPOINT,json=request_body,headers=headers)

    if response.status_code == 202 :
        return {"status_code" : 202,"message" : "Mail sent"}
    
    elif response.status_code == 400 :
        return {"status_code" : 400,"message" : "Invalid base64 string for MIME content" }
    
    else :
        return {"status_code" : response.status_code,"message" : response.json()}
    


def list_messages(select="",top="",filter="",save_dir="") :

    #It will list first 10 messages in mailbox
    API_ENDPOINT = "https://graph.microsoft.com/v1.0/me/messages"

    headers = {
                    "Authorization" : "Bearer " + os.environ["ACCESS_TOKEN"],
                    "Content-Type" : "application/json"
    }

    params = {}

    if select :
        params["select"] = select
    if top : 
        params["top"] = top
    if filter :
        params["filter"] = filter
    


    response = requests.get(API_ENDPOINT,params=params,headers=headers)

    if not response.status_code == 200 :
        return {"status_code" : response.status_code,"message" : response.json()}
    
    emails = response.json()["value"]

    formatted_mail_list = []

    for email in emails :
        if email["hasAttachments"] :
            email["attachmnets_path_list"] = download_attachments(email["id"],headers)
            formatted_mail_list.append(email)
        else :
            formatted_mail_list.append(email)

    return formatted_mail_list
        




def list_message_from_mail_folder(folderId="inbox",select="",top="",filter="",save_dir="") :

    API_ENDPOINT = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folderId}/messages"

    headers = {
                    "Authorization" : "Bearer " + os.environ["ACCESS_TOKEN"],
                    "Content-Type" : "application/json"
    }

    params = {}

    if select :
        params["select"] = select
    if top : 
        params["top"] = top
    if filter :
        params["filter"] = filter
        


    response = requests.get(API_ENDPOINT,params=params,headers=headers)

    if not response.status_code == 200 :
        return {"status_code" : response.status_code,"message" : response.json()}
    
    emails = response.json()["value"]

    formatted_mail_list = []

    for email in emails :
        if email["hasAttachments"] :
            email["attachmnets_path_list"] = download_attachments(email["id"],headers)
            formatted_mail_list.append(email)
        else :
            formatted_mail_list.append(email)

    return formatted_mail_list
        






