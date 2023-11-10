import requests
import const


def request_access_token():
    url = "https://api.amazon.com/auth/o2/token"
    
    # Define the request body
    data = {
        "grant_type": "refresh_token",
        "client_id": const.LWA_APP_ID,
        "refresh_token": const.REFRESH_TOKEN,
        "client_secret": const.CLIENT_SECRET,
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    
    # Send the POST request
    response = requests.post(url, data=data, headers=headers)
    
    if response.ok:
        return response.json()
    else:
        raise Exception(response.reason)  # You can change the exception type if needed

try:
    token_data = request_access_token()
    #print(token_data["access_token"])
except Exception as e:
    print(f"Error: {e}")
