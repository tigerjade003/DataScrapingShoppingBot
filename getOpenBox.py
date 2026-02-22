from curl_cffi import requests
import time

IMPERSONATE = "chrome"
USER_AGENTS = {
    "chrome120": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "chrome110": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}


def fetch_condition(session, url, sku, vt, condition):
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
    }

    json_data = {
        'operationName': 'getProduct',
        'variables': {
            'skuId': sku,
            'openBoxCondition': condition,
        },
        'query': f'query getProduct($skuId: String!, $openBoxCondition: Int) {{\n  productBySkuId(skuId: $skuId, openBoxCondition: $openBoxCondition) {{\n    ...priceXProductFragment\n    __typename\n    skuId\n    openBoxCondition\n  }}\n}}\n\nfragment priceXProductFragment on Product {{\n  skuId\n  name {{\n    short\n    __typename\n  }}\n  price(\n    input: {{salesChannel: "LargeView", usePriceWithCart: true, cartTimestamp: "1771475979748", visitorId: "{vt}", useCabo: true, useSuco: true}}\n  ) {{\n    __typename\n    openBoxPrice\n    openBoxSavings\n    openBoxCondition\n    lowestOpenboxPrice\n    displayableCustomerPrice\n    displayableRegularPrice\n    totalSavings\n    totalSavingsPercent\n  }}\n  __typename\n  openBoxCondition\n}}',
    }

    response = session.post(
        'https://www.bestbuy.com/gateway/graphql',
        json=json_data,
        headers=headers,
    )
    return response.json()


def get_data(url, sku):
    session = requests.Session(impersonate=IMPERSONATE)
    all_data = [-1, -1, -1, -1]
    home_response = session.get('https://www.bestbuy.com')
    vt = home_response.cookies.get('vt')
    time.sleep(2)
    name = None
    for condition in range(0, 3): # 0 = Fair, 1 = Good, 2 = Like New
        try:
            data = fetch_condition(session, url, sku, vt, condition)
            product = data['data']['productBySkuId']

            if product is None:
                continue
            if name is None:
                name = product['name']['short']
            if all_data[3] == -1:
                all_data[3] = product['price']['displayableRegularPrice']
            price = product['price']
            all_data[condition] = price['openBoxPrice']
        except Exception as e:
            print(f"\n[{condition}] Failed to fetch: {e}")

        time.sleep(0.2)  # small delay between requests
    return name, all_data


print(get_data(
    url="https://www.bestbuy.com/product/lenovo-legion-7i-16-2-5k-lcd-gaming-laptop-intel-14th-gen-core-i7-with-16gb-memory-nvidia-geforce-rtx-4060-8gb-1tb-ssd-glacier-white/JJGYCCVGWJ/sku/6575391/openbox?condition=fair",
    sku="6575391",
))