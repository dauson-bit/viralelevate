import requests
import base64
from datetime import datetime
import json
from django.conf import settings

class MpesaAPI:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.passkey = settings.MPESA_PASSKEY
        self.shortcode = settings.MPESA_SHORTCODE
        self.callback_url = settings.MPESA_CALLBACK_URL
        self.base_url = "https://sandbox.safaricom.co.ke" if settings.DEBUG else "https://api.safaricom.co.ke"

    def get_access_token(self):
        """Get M-PESA API access token"""
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["access_token"]
        return None

    def initiate_stk_push(self, phone_number, amount, order_id):
        """Initiate STK Push to customer's phone"""
        access_token = self.get_access_token()
        if not access_token:
            return {"status": "error", "message": "Failed to get access token"}

        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(
            f"{self.shortcode}{self.passkey}{timestamp}".encode()
        ).decode()

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": f"{self.callback_url}/mpesa/callback/{order_id}/",
            "AccountReference": f"Order {order_id}",
            "TransactionDesc": "Payment for order"
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "checkout_request_id": response_data.get("CheckoutRequestID"),
                    "message": "STK Push initiated successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": response_data.get("errorMessage", "Failed to initiate payment")
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def check_transaction_status(self, checkout_request_id):
        """Check the status of an STK Push transaction"""
        access_token = self.get_access_token()
        if not access_token:
            return {"status": "error", "message": "Failed to get access token"}

        url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(
            f"{self.shortcode}{self.passkey}{timestamp}".encode()
        ).decode()

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "result_code": response_data.get("ResultCode"),
                    "result_desc": response_data.get("ResultDesc")
                }
            else:
                return {
                    "status": "error",
                    "message": response_data.get("errorMessage", "Failed to check transaction status")
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            } 