from curl_cffi import requests
import time

IMPERSONATE = "chrome"
USER_AGENTS = {
    "chrome120": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "chrome110": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

def get_data(url, sku, open_box_condition=None):
    session = requests.Session(impersonate=IMPERSONATE)
    
    # Get fresh cookies including vt and basketTimestamp
    home_response = session.get('https://www.bestbuy.com')
    vt = home_response.cookies.get('vt')
    cart_timestamp = home_response.cookies.get('basketTimestamp')
    time.sleep(2)

    print(f"vt: {vt}")
    print(f"cartTimestamp: {cart_timestamp}")

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,zh;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.bestbuy.com',
        'priority': 'u=1, i',
        'referer': url,
        'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': USER_AGENTS[IMPERSONATE],
        'x-client-id': 'pdp-web',
        'x-dynatrace': '',
        'x-requested-for-operation-name': 'getProduct',
        'cookie': f'vt={vt};'
    }

    json_data = {
        'operationName': 'getProduct',
        'variables': {
            'skuId': sku,
            'openBoxCondition': open_box_condition,
        },
        'query': f'query getProduct($skuId: String!, $openBoxCondition: Int) {{\n  productBySkuId(skuId: $skuId, openBoxCondition: $openBoxCondition) {{\n    ...priceXProductFragment\n    __typename\n    skuId\n    openBoxCondition\n  }}\n}}\n\nfragment priceXProductFragment on Product {{\n  skuId\n  name {{\n    short\n    __typename\n  }}\n  price(\n    input: {{salesChannel: "LargeView", usePriceWithCart: true, cartTimestamp: "1771475979748", visitorId: "{vt}", useCabo: true, useSuco: true}}\n  ) {{\n    __typename\n    openBoxPrice\n    openBoxSavings\n    openBoxCondition\n    lowestOpenboxPrice\n    displayableCustomerPrice\n    displayableRegularPrice\n    totalSavings\n    totalSavingsPercent\n  }}\n  __typename\n  openBoxCondition\n}}',
    }

    response = session.post(
        'https://www.bestbuy.com/gateway/graphql',
        json=json_data,
        headers=headers,
    )

    data = response.json()
    product = data['data']['productBySkuId']
    name = product['name']['short']
    price = product['price']

    print(f"Product: {name}")
    print(f"Open Box Condition: {product['openBoxCondition']}")
    print(f"Open Box Price: ${price['openBoxPrice']}")
    print(f"Open Box Savings: ${price['openBoxSavings']}")
    print(f"Lowest Open Box Price: ${price['lowestOpenboxPrice']}")
    print(f"Regular Price: {price['displayableRegularPrice']}")

get_data(
    url="https://www.bestbuy.com/product/lenovo-legion-7i-16-2-5k-lcd-gaming-laptop-intel-14th-gen-core-i7-with-16gb-memory-nvidia-geforce-rtx-4060-8gb-1tb-ssd-glacier-white/JJGYCCVGWJ/sku/6575391/openbox?condition=fair",
    sku="6575391",
    # 0 = bad, 1 = fair, 2 = good
    open_box_condition=2
)