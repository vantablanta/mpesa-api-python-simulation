import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import os 
from dotenv import load_dotenv
load_dotenv()


# generate time stamp 
unformatted_time = datetime.now()
formatted_time = unformatted_time.strftime('%Y%m%d%H%M%S')

# generate password 
passkey = os.getenv("PASSKEY")
shortcode = os.getenv("BUSINESS_SHORTCODE")
string_to_encode = shortcode + passkey + formatted_time

# encode password 
encoded_password = base64.b64encode(string_to_encode.encode())
my_password = encoded_password.decode('utf-8')

# get auth token 
auth_url = os.getenv("AUTH_ENDPOINT")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
my_auth = requests.get(auth_url, auth=HTTPBasicAuth(consumer_key,consumer_secret))
my_access_token = my_auth.json()["access_token"]

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer'+ " "+ my_access_token
}
payload = {
    "BusinessShortCode": int(os.getenv("BUSINESS_SHORTCODE")),
    "Password": my_password,
    "Timestamp": formatted_time,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254796693270,
    "PartyB": int(os.getenv("BUSINESS_SHORTCODE")),
    "PhoneNumber": 254796693270,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "Michelle ",
    "TransactionDesc": "Payment of Fees" 
  }

response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json = payload)
print(response.text.encode('utf8'))