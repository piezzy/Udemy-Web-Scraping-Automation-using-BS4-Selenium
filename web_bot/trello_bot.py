from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import date
import os
import json

CHROME_DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
OP = Options()
# OP.add_argument("--headless")
OP.add_argument("--start-maximized")
service = Service(CHROME_DRIVER_PATH)
DRIVER = webdriver.Chrome(service=service, options=OP)

def login():
    with open ("config.json", "r") as f:
        credentials = json.load(f)
        time.sleep(2)
        DRIVER.find_element(By.XPATH, value="//a[contains(@href, 'id.atlassian.com/login')]").click()
        print(credentials) # dbgging
        
def main():
    try:
        DRIVER.get("https://trello.com/")
        login()
        input("bot operation completed, press any key to exit")
        DRIVER.quit()
        
    except Exception as e:
        print("Error: ", e)
        
if __name__ == "__main__":
    main()