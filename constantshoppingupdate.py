from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import json
import ShoppingNotificationBot
import time

chrome_options = uc.ChromeOptions()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
#chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=chrome_options)

try:
    url = "https://www.bestbuy.com/product/lenovo-ideapad-slim-3-15-6-full-hd-touchscreen-laptop-amd-ryzen-7-5825u-2025-16gb-memory-512gb-ssd-arctic-grey/JJGSH2ZQWS"
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    soup = BeautifulSoup(driver.page_source, "html.parser")

    scripts = soup.find_all("script", {"type": "application/ld+json"})

    product_name = None
    price = None

    for script in scripts:
        try:
            data = json.loads(script.string)
#type="application/ld+json">{"@context":"http://schema.org/","@type":"Product","name":"Lenovo - IdeaPad Slim 3 15.6\" Full HD Touchscreen Laptop - AMD Ryzen 7 5825U 2025 - 16GB Memory - 512GB SSD - Arctic Grey","image":[],"url":"https://www.bestbuy.com/product/lenovo-ideapad-slim-3-15-6-full-hd-touchscreen-laptop-amd-ryzen-7-5825u-2025-16gb-memory-512gb-ssd-arctic-grey/JJGSH2ZQWS","description":null,"sku":"11357527","model":"82XM00LMUS","color":"Arctic Grey","brand":{"@type":"Brand","name":"Lenovo"},"aggregateRating":{"@type":"AggregateRating","ratingValue":4.8,"reviewCount":1907,"url":"https://www.bestbuy.com/site/reviews/name/11357527"},"offers":[{"@type":"Offer","priceCurrency":"USD","price":518,
            if isinstance(data, list):
                data = data[0]

            if data.get("@type") == "Product":
                product_name = data.get("name")
                price = float(data.get("offers", {}).get("price", 0))
                break
        except:
            continue

    if product_name and price:
        print(f"Product: {product_name}")
        print(f"Price: ${price}")
        ShoppingNotificationBot.check_event(product_name, price, 550)
    else:
        print("Could not find product data in JSON-LD")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    time.sleep(5)
    driver.quit()