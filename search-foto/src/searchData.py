import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

class SearchData:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        options = webdriver.SafariOptions()
        self.driver = webdriver.Safari(options=options)

    def login(self, site_url):
        if self.username and self.password:
            try:
                self.driver.get(site_url)
                username_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, 'username'))
                )
                username_input.clear()
                username_input.send_keys(self.username)
                time.sleep(random.uniform(2, 3))

                password_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, 'password'))
                )
                password_input.clear()
                password_input.send_keys(self.password)
                password_input.send_keys(self.password)
                password_input.send_keys(Keys.ENTER)
                time.sleep(random.uniform(2, 3))
            except Exception as e:
                logging.error(f"Error logging in to {site_url}: {e}")
        else:
            logging.info(f"Skipping login for {site_url} as username or password is not provided.")

    def search_user(self, username, site_url):
        self.driver.get(f'{site_url}/{username}/')

    def scroll_and_collect_images(self):
        image_urls = set()
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            images = soup.find_all('img')
            for img in images:
                img_url = img.get('src')
                if img_url and img_url not in image_urls:
                    image_urls.add(img_url)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 5))
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return list(image_urls)

    def close(self):
        self.driver.quit()