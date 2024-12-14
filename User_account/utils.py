import requests
import os 
api_key =os.environ.get('2factor_API_key')

def send_sms(phone_number): 
    print(api_key)
    url = f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/AUTOGEN2/OTP1"
          
    payload={}
    headers = {}
 
    response = requests.request("GET", url, headers=headers, data=payload)
 
    print(response.text)
    return response


def verify_sms_phone_no(otp,phone_no):
    url = f"https://2factor.in/API/V1/{api_key}/SMS/VERIFY3/{phone_no}/{otp}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return response


