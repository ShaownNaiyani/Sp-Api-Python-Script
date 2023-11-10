import requests
from requests_aws4auth import AWS4Auth


def get_catalog_item(marketplace_id, asin, access_token, credentials):
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]

    path = f"/catalog/2022-04-01/items/{asin}?marketplaceIds={marketplace_id}&includedData=attributes,identifiers,images,productTypes,salesRanks,summaries"
    method = 'GET'
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

    # Send the signed request
    response = requests.get(url, auth=auth, headers={'x-amz-access-token': access_token})

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code {response.status_code}")



