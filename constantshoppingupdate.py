from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import json
import ShoppingNotificationBot

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--headless")
# these are for additional secrecy when the scraper goes and looks at prices. - if it cannot find the price or name, uncomment these. 
#chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
#chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=chrome_options)
url = "https://www.bestbuy.com/product/lenovo-ideapad-slim-3-15-6-full-hd-touchscreen-laptop-amd-ryzen-7-5825u-2025-16gb-memory-512gb-ssd-arctic-grey/JJGSH2ZQWS"
driver.get(url)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)
soup = BeautifulSoup(driver.page_source, "html.parser")
scripts = soup.find_all("script", {"type": "application/ld+json"})

for i, script in enumerate(scripts):
    print(f"--- Block {i} ---")
    data = json.loads(script.string)
    print(json.dumps(data, indent=2))
def get_price(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    soup = BeautifulSoup(driver.page_source, "html.parser")
    scripts = soup.find_all("script", {"type": "application/ld+json"})
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                data = data[0]
            if data.get("@type") == "Product":
                offers = data.get("offers", [])
                if isinstance(offers, list):
                    price = float(offers[0].get("price", 0))
                else:
                    price = float(offers.get("price", 0))
                return price
        except:
            continue

def get_name(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    soup = BeautifulSoup(driver.page_source, "html.parser")
    scripts = soup.find_all("script", {"type": "application/ld+json"})
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                data = data[0]
            if data.get("@type") == "Product":
                return data.get("name")
        except:
            continue
    return None

print(get_name(url))
print(get_price(url))