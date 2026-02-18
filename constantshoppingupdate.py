# get prices - first do best buy
# then find a way to keep it in the cart + never lose it
# have a way to copy the cookies
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import ShoppingNotificationBot

time.sleep(3)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=chrome_options)


while True:
    try:
        url = "https://www.bestbuy.com/product/lenovo-ideapad-slim-3-15-6-full-hd-touchscreen-laptop-amd-ryzen-7-5825u-2025-16gb-memory-512gb-ssd-arctic-grey/JJGSH2ZQWS"
        driver.get(url) 
        wait = WebDriverWait(driver, 10)
        product_header_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-component-name='ProductHeader']"))
        )
        price_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='price-block-customer-price']"))
        )
        title_element = product_header_container.find_element(By.CLASS_NAME, "h4")
        product_name = title_element.text.strip()
        price_text = price_element.get_attribute("aria-label")
        print(f"The product name is: {product_name}")
        print(f"The price is: {price_text}")
        ShoppingNotificationBot.check_event(product_name, float(price_text[1:]), 550)
        time.sleep(600)

    except Exception as e:
        print(f"An error occurred: {e}")


