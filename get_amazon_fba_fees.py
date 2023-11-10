import requests
from requests_aws4auth import AWS4Auth
import json


def get_amazon_fba_fees(asin, list_price, access_token, credentials):
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]
    payload = {
        "FeesEstimateRequest": {
            "MarketplaceId": "A2EUQ1WTGCTBG2",
            "PriceToEstimateFees": {
                "ListingPrice": {
                    "CurrencyCode": "CAD",
                    "Amount": list_price
                },
                "Shipping": {
                    "CurrencyCode": "CAD",
                    "Amount": 0
                },
                "Points": {
                    "PointsNumber": 0,
                    "PointsMonetaryValue": {
                        "CurrencyCode": "CAD",
                        "Amount": 0
                    }
                }
            },
            "Identifier": "sh224",
            "IsAmazonFulfilled": "true"
        }
    }
    body = json.dumps(payload)

    headers = {
        'User-Agent': 'MyAmazonApp/1.0 (Language=JavaScript;)',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-amz-access-token': access_token,
    }

    path = f"/products/fees/v0/items/{asin}/feesEstimate"
    method = 'POST'
    host = 'sellingpartnerapi-na.amazon.com'
    region = 'us-east-1'

    auth = AWS4Auth(
        access_key_id,
        secret_access_key,
        region,
        method,
        'execute-api',
        session_token=session_token
    )
    url = f"https://{host}{path}"

    response = requests.post(url, auth=auth, headers=headers, data=body)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Request failed with status code {response.status_code}")
