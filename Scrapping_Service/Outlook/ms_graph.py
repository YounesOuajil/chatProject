import webbrowser
from datetime import datetime
import json
import os
import msal

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

def generate_access_token(app_id, scopes, id_internship):
    try:
        # Save Session Token as a token file
        access_token_cache = msal.SerializableTokenCache()

        # read the token file
        if os.path.exists('ms_graph_api_token.json'):
            access_token_cache.deserialize(open("ms_graph_api_token.json", "r").read())
            token_detail = json.load(open('ms_graph_api_token.json',))
            token_detail_key = list(token_detail['AccessToken'].keys())[0]
            token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
            if datetime.now() > token_expiration:
                os.remove('ms_graph_api_token.json')
                access_token_cache = msal.SerializableTokenCache()

        # assign a SerializableTokenCache object to the client instance
        client = msal.PublicClientApplication(client_id=app_id, token_cache=access_token_cache)

        accounts = client.get_accounts()
        if accounts:
            # load the session
            token_response = client.acquire_token_silent(scopes, accounts[0])
        else:
            # authenticate your account as usual
            flow = client.initiate_device_flow(scopes=scopes)
            if 'user_code' in flow:
                 # Load existing user codes
                user_codes = {}
                if os.path.exists('user_code.json'):
                    with open('user_code.json', 'r') as f:
                        user_codes = json.load(f)
                
                # Update user codes with the new one
                user_codes[f'user_code_{id_internship}'] = flow['user_code']
                
                # Write updated user codes back to the file
                with open('user_code.json', 'w') as f: 
                    json.dump(user_codes, f)

                print('user_code: ' + flow['user_code'])
                webbrowser.open(flow['verification_uri'])
                print('Please follow the instructions on the webpage to complete the authentication.')
                # input('Press Enter to continue after completing the authentication...')
                token_response = client.acquire_token_by_device_flow(flow)
            else:
                print('Failed to initiate device flow. Response:', flow)
                return None

        with open('ms_graph_api_token.json', 'w') as _f:
            _f.write(access_token_cache.serialize())

        return token_response
    except Exception as e:
        print('An error occurred:', e)
        return None

# def save_user_code(user_code):
#     # Save the user_code to a file or database
#     with open('user_code.json', 'w') as f:
#         json.dump({'user_code': user_code}, f)

# if __name__ == '__main__':
#     APP_ID = '349979d8-e863-4fe4-97ea-e3361699b7af'
#     SCOPES = ['Mail.ReadWrite']
    
#     access_token = generate_access_token(app_id=APP_ID, scopes=SCOPES)
#     if access_token:
#         print('Access token:', access_token)
#     else:
#         print('Failed to obtain access token.')
