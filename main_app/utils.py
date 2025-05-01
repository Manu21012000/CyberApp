from django.conf import settings
from twilio.rest import Client
import requests
import json

def send_sms_verification_code(phone_number, verification_code):
    """
    Send verification code via SMS using Twilio
    """
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your verification code is: {verification_code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=str(phone_number)
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)

def send_whatsapp_verification_code(phone_number, verification_code):
    """
    Send verification code via WhatsApp using WhatsApp Business API
    """
    try:
        url = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": str(phone_number),
            "type": "template",
            "template": {
                "name": "verification_code",
                "language": {
                    "code": "en"
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": verification_code
                            }
                        ]
                    }
                ]
            }
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        return False, str(e)

def send_verification_code(phone_number, verification_code, method='sms'):
    """
    Send verification code using the specified method
    """
    if method == 'sms':
        return send_sms_verification_code(phone_number, verification_code)
    elif method == 'whatsapp':
        return send_whatsapp_verification_code(phone_number, verification_code)
    else:
        return False, "Invalid verification method" 