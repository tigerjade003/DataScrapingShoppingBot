import http.client
import json
from curl_cffi import requests

# Step 1: Get fresh cookies from Best Buy
session = requests.Session(impersonate="chrome120")
session.get('https://www.bestbuy.com')
cookies = {name: value for name, value in session.cookies.items()}

# Step 2: Build cookie string from fresh cookies
cookie_string = '; '.join([f'{name}={value}' for name, value in cookies.items()])
print(cookie_string)
# Step 3: Make the GraphQL request
conn = http.client.HTTPSConnection('www.bestbuy.com')
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,zh;q=0.8',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://www.bestbuy.com',
    'priority': 'u=1, i',
    'referer': 'https://www.bestbuy.com/product/lenovo-ideapad-slim-3-15-6-full-hd-touchscreen-laptop-amd-ryzen-7-5825u-2025-16gb-memory-512gb-ssd-arctic-grey/JJGSH2ZQWS',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'x-client-id': 'pdp-web',
    'x-dynatrace': '',
    'x-requested-for-operation-name': 'getPDPProductBySkuId',
    'cookie': cookie_string,
}

json_data = {
    'operationName': 'getPDPProductBySkuId',
    'variables': {
        'skuId': '11925192',
    },
    'query': 'query getPDPProductBySkuId($skuId: String!) {\n  productBySkuId(skuId: $skuId) {\n    brand\n    name {\n      short\n      __typename\n    }\n    price(input: {salesChannel: "www"}) {\n      currentPrice\n      __typename\n    }\n    __typename\n    skuId\n  }\n}',
}

conn.request('POST', '/gateway/graphql', json.dumps(json_data), headers)
response = conn.getresponse()
data = json.loads(response.read().decode('utf-8'))
print(json.dumps(data, indent=2))