import requests

# Assuming your Django backend is hosted locally
url = "http://127.0.0.1:8000/ai/user_code_view/"

# Data to send to the backend
data = {"user_code": "teeeeesssst"}

# Making a POST request to the backend
response = requests.post(url, json=data)

# Handling the response from the backend
if response.status_code == 200:
    # Request was successful, process the response data
    response_data = response.json()
    print("Response from backend:", response_data)
else:
    # Request failed, handle the error
    print("Error:", response.status_code)
