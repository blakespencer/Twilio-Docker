import os
import requests
import uuid
import json
try:
    from secrets import subscription_key
except:
    subscription_key = os.environ['SUBSCRIPTION_KEY']


def get_sentiment(input_text):
    base_url = 'https://westcentralus.api.cognitive.microsoft.com/text/analytics'
    path = '/v2.0/sentiment'
    constructed_url = base_url + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = {
        'documents': [
            {
                'language': 'en',
                'id': '1',
                'text': input_text
            },
        ]
    }
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()
