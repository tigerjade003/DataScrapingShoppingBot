from curl_cffi import requests

# Step 1: Get fresh cookies
session = requests.Session(impersonate="chrome120")
session.get('https://www.bestbuy.com')

# Step 2: Make the GraphQL request with the same session (cookies auto-attached)
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,zh;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://www.bestbuy.com',
    'referer': 'https://www.bestbuy.com',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-client-id': 'pdp-web',
    'x-requested-for-operation-name': 'getPDPProductBySkuId',
}

json_data = {
    'operationName': 'getPDPProductBySkuId',
    'variables': {
        'skuId': '11925192',
    },
    'query': 'query getPDPProductBySkuId($skuId: String!) {\n  productBySkuId(skuId: $skuId) {\n    brand\n    name {\n      short\n      __typename\n    }\n    price(input: {salesChannel: "www"}) {\n      currentPrice\n      __typename\n    }\n    __typename\n    skuId\n  }\n}',
}

response = session.post(
    'https://www.bestbuy.com/gateway/graphql',
    json=json_data,
    headers=headers
)

import json
print(json.dumps(response.json(), indent=2))