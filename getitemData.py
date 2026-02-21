from curl_cffi import requests
IMPERSONATE = "chrome"
USER_AGENTS = {
    "chrome120": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "chrome110": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}
def get_data(url):
    session = requests.Session(impersonate=IMPERSONATE)
    response = session.get('https://www.bestbuy.com')
    vt = response.cookies.get('vt')
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,zh;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.bestbuy.com',
        'priority': 'u=1, i',
        'referer': f'{url}',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': USER_AGENTS[IMPERSONATE],
        'x-akamai-edgescape': 'georegion=246,country_code=US,region_code=CA,city=IRVINE,dma=803,pmsa=5945,msa=4472,areacode=949+714,county=ORANGE,fips=06059,lat=33.6880,long=-117.7988,timezone=PST,zip=92602-92604+92606+92612+92614+92616+92618-92620+92623+92697,continent=NA,throughput=vhigh,bw=5000,asnum=16591,location_id=0',
        'x-client-id': 'pdp-web',
        'x-dynatrace': '',
        'x-page-request-id': '01ac129b-41b1-4bae-bf31-9b5bd0625a65',
        'x-request-id': 'xrequest::1771556073::23.213.247.110::5542a038::1597550',
        'x-requested-for-operation-name': 'getPDPProductBySkuId',
        'cookie': f'vt={vt};'
    }
    print(vt)
    json_data = {
        'operationName': 'getPDPProductBySkuId',
        'variables': {
            'skuId': '11925192',
        },
        'query': 'query getPDPProductBySkuId($skuId: String!) {\n  productBySkuId(skuId: $skuId) {\n    brand\n    hierarchy {\n      bbypres {\n        primary\n        id\n        categoryDetail {\n          name\n          broaderTerms {\n            primaryLineage {\n              id\n              name\n              sequence\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    name {\n      short\n      __typename\n    }\n    price(input: {salesChannel: "www"}) {\n      currentPrice\n      __typename\n    }\n    reviewInfo {\n      averageRating\n      __typename\n    }\n    __typename\n    skuId\n    openBoxCondition\n  }\n}',
    }
    response = session.post(
        'https://www.bestbuy.com/gateway/graphql',
        json=json_data,
        headers=headers,
    )
    data = response.json()
    product = data['data']['productBySkuId']
    name = product['name']['short'] 
    price = product['price']['currentPrice']
    print(f"Product: {name}")
    print(f"Price: ${price}")

get_data("https://www.bestbuy.com/product/lenovo-ideapad-slim-3-15-6-full-hd-touchscreen-laptop-amd-ryzen-7-5825u-2025-16gb-memory-512gb-ssd-arctic-grey/JJGSH2ZQWS")