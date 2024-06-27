Email Attachment Extraction Project: Outlook
Overview

This project aims to automate the extraction of email attachments from Microsoft Outlook using the Microsoft Graph API. It retrieves unread emails with a specific subject and extracts attachments from them.
Features

    Extract attachments from unread emails with a specific subject.
    Mark processed emails as read to avoid duplicate extraction.

Prerequisites

    Python 3.x installed on your system.
    Microsoft Outlook account with access to the Microsoft Graph API.
    Registered Azure AD application with appropriate permissions.

Setup

    Clone the repository to your local machine.
    Install dependencies by running pip install -r requirements.txt.
    Configure your Azure AD application and obtain the required credentials (client ID, client secret).
    Update the APP_ID variable in demo.py with your Azure AD application's client ID.
    Run the demo.py script to start extracting attachments from unread emails.

Usage

    Modify the subject filter in the demo.py script to target specific emails.
    Customize the save folder for extracted attachments by updating the save_folder parameter in the download_email_attachments function.
    Execute the script periodically using a scheduler (e.g., cron job) to automate the extraction process.

OAuth

    Using (OAuth and the App ID). This approach allows you to use the same App ID to authenticate with different Outlook accounts, providing flexibility in accessing different email accounts without needing to create separate apps for each account.

Troubleshooting

If you encounter any issues or errors while running the script, refer to the troubleshooting section in the README file or seek assistance from the project contributors.
Contributors

AKAABOUR OUSSAMA (akaabouroussama@gmail.com)

Note:

time life of an access token
Token expiration date and time: 2024-04-29 11:42:39
Token expiration date and time: 2024-04-29 12:52:43

error:
KeyError: ‘user_code'

 Solution: I was able to fix this by switching the App platform to Public client/native (mobile & desktop) in Azure App Registration. I had to create a new app because I don’t think there’s a way to change the existing one.

 how to create APP_ID:

 create an app(mobile & desktop) "https://portal.azure.com" with the microsoft email you want and get your appID
(The step of registering your application typically needs to be done manually through the Microsoft Azure)

ytb: https://www.youtube.com/watch?v=1Jyd7SA-0kI
steps:
create app (web or mobile) : for url: http://localhost:8000/callback
add permessions api : email, Mail.Read, Mail.ReadBasic, Mail.ReadWrite, openid, User.Read
go to authentication: make the two settings YES
and save 
note that for some types of outlook account you can't find the 'app registration' option!!