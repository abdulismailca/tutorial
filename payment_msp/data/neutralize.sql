UPDATE payment_provider
   SET multisafepay_api_key = NULL;


import requests

url = "https://testapi.multisafepay.com/v1/json/orders?api_key=7caeed9a6b8e4efff21a9b8a9e6a51f274f0cb3c"

payload = {
    "payment_options": {
        "close_window": False,
        "notification_method": "POST",
        "notification_url": "https://www.example.com/webhooks/payment",
        "redirect_url": "https://www.example.com/order/success",
        "cancel_url": "https://www.example.com/order/failed"
    },
    "customer": {
        "locale": "en_US",
        "disable_send_email": False
    },
    "checkout_options": { "validate_cart": False },
    "days_active": 30,
    "seconds_active": 2592000,
    "type": "redirect",
    "order_id": "my-order-id-1",
    "currency": "EUR",
    "amount": 37485,
    "description": "Test Order Description"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)