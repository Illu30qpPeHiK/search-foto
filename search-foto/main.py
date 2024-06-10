import os
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

class SearchBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        options = webdriver.SafariOptions()
        self.driver = webdriver.Safari(options=options)

    def login(self):
        try:
            self.driver.get('https://www.instagram.com/')
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
            logging.error(f"Error logging in: {e}")

    def search_user(self, username):
        self.driver.get(f'https://www.instagram.com/{username}/')

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


class ImageDownloader:
    def __init__(self, folder):
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

    def download_images(self, image_urls):
        for index, img_url in enumerate(image_urls):
            if img_url:
                try:
                    img_data = requests.get(img_url).content
                    with open(f"{self.folder}/image_{index + 1}.jpg", 'wb') as handler:
                        handler.write(img_data)
                    logging.info(f"Image {index + 1} downloaded: {img_url} \n")
                except Exception as e:
                    logging.error(f"Could not download image {img_url}: {e} \n")


def main():
    username = os.getenv('username')
    password = os.getenv('password')
    
    bot = SearchBot(username, password)
    downloader = ImageDownloader(folder=username_to_search)
    
    if not username or not password:
        try:
            username_to_search = input('Enter the username that needs to be found: ')
            bot.search_user(username_to_search)

            image_urls = bot.scroll_and_collect_images()

            bot.close()

            if image_urls:
                downloader.download_images(image_urls)
            else:
                logging.info("No images found for the given username.")
        
            time.sleep(random.uniform(2, 5))

        except Exception as e:
            logging.error(f"Please set the username and password as environment variables: {e}")

    else:
        try:
            bot.login()

            username_to_search = input('Enter the username that needs to be found: ')

            bot.search_user(username_to_search)

            image_urls = bot.scroll_and_collect_images()

            bot.close()

            if image_urls:
                downloader.download_images(image_urls)
            else:
                logging.info("No images found for the given username.")
        
            time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            logging.error(f"Error: {e}")
    

if __name__ == "__main__":
    main()
