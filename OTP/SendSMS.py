from twilio.rest import Client
import json
with open('.\OTP\keys.json', 'r') as file:
    keys = json.load(file)
  
account_sid = keys['account_sid']
auth_token = keys['auth_token']
verify_sid = keys['verify_sid']
verified_number = "+21625448116"

client = Client(account_sid, auth_token)

verification = client.verify.v2.services(verify_sid) \
  .verifications \
  .create(to=verified_number, channel="sms")
print(verification.status)

otp_code = input("Please enter the OTP:")

verification_check = client.verify.v2.services(verify_sid) \
  .verification_checks \
  .create(to=verified_number, code=otp_code)
print(verification_check.status)
