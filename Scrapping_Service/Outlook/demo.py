import os
import requests
from ms_graph import generate_access_token

def download_email_attachments(message_id, headers, save_folder=os.getcwd()):
    GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'
    try:
        response = requests.get(
            GRAPH_API_ENDPOINT + '/me/messages/{0}/attachments'.format(message_id),
            headers=headers
        )

        attachment_items = response.json()['value']
        for attachment in attachment_items:
            file_name = attachment['name']
            attachment_id = attachment['id']
            attachment_content = requests.get(
                GRAPH_API_ENDPOINT + '/me/messages/{0}/attachments/{1}/$value'.format(message_id, attachment_id),
                headers=headers
            )
            from datetime import datetime
            # Append current date and time to filename
            base, extension = os.path.splitext(file_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"{base}_{timestamp}{extension}"
            
            print('Saving file {0}...'.format(unique_filename))
            with open(os.path.join(save_folder, unique_filename), 'wb') as _f:
                _f.write(attachment_content.content)
        
        # Mark the email as seen after extracting attachments
        patch_url = GRAPH_API_ENDPOINT + '/me/messages/{0}'.format(message_id)
        patch_data = {
            'isRead': True
        }
        response = requests.patch(patch_url, headers=headers, json=patch_data)
        if response.status_code != 204:
            print('Failed to mark email as read:', response.text)
        
        return True
    except Exception as e:
        print(e)
        return False
    

def handle_Scrapping(sujet, id_internship):
    import os
    # Step 1. Get the access token
    APP_ID = 'f9cfb900-c795-4cda-b391-16070348a48e'
    # APP_ID = 'b04c3710-725e-4c51-9d96-2671e6347ae1'
    SCOPES = ['Mail.ReadWrite']
    GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

    folder_path = 'C:/Users/pc/Desktop/Stage_PULSE/codes/BackEnd/Project_django/Scrapping_Service/Attachments'
    folder_path_temp = 'C:/Users/pc/Desktop/Stage_PULSE/codes/BackEnd/Project_django/Scrapping_Service/Temporary_Attachments'

    access_token = generate_access_token(app_id=APP_ID, scopes=SCOPES, id_internship=id_internship)
    os.remove('ms_graph_api_token.json')
    headers = {
        'Authorization': 'Bearer ' + access_token['access_token']
    }

    # Step 2. Retrieve unseen emails with specific subject
    params = {
        'top': 3,  # max is 1000 messages per request
        'select': 'id,subject,hasAttachments',
        'filter': f'isRead eq false and subject eq \'{sujet}\' and hasAttachments eq true',
        'count': 'true'
    }

    response = requests.get(GRAPH_API_ENDPOINT + '/me/mailFolders/inbox/messages', headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(response.json())

    response_json = response.json()
    emails = response_json['value']

    # Step 3. Download attachments from filtered unseen emails
    if emails:
        for email in emails:
            email_id = email['id']
            download_email_attachments(email_id, headers, folder_path)
            download_email_attachments(email_id, headers, folder_path_temp)
            
    else:
        print(" No attachments scrapped!!.")


    #  Step 4. Parsing the Resumes and save them in DB
    if os.listdir(folder_path_temp):
        import os
        import sys
        # Add the parent directory to the system path
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

        from Resume_Parsing.main import Resume_Parsing_to_DB

        for filename in os.listdir(folder_path_temp):
            if filename.endswith('.pdf'):  
                resume_path_temp = os.path.join(folder_path_temp, filename)
                reference = 'Attachment/' + str(filename)
                Resume_Parsing_to_DB(resume_path_temp, sujet, reference,id_internship)
                os.remove(resume_path_temp)

    else: 
        print("The folder of Reumes is empty. No resumes to parse.")

