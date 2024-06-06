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
from auth_data import username, password

driver = webdriver.Safari()

def search_user():
    return input('Введіть username котрий треба знайти: ')

def login(username, password):
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    username_input.clear()
    username_input.send_keys(username)
    time.sleep(random.randrange(2, 5))

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_input.send_keys(password)
    password_input.clear()
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(random.randrange(2, 5))

def search(username):
    driver.get(f'https://www.instagram.com/{username}/')

def get_page_source():
    time.sleep(random.randrange(2, 5)) 
    return driver.page_source

def get_all_fotos(page_source):
    try:
        soup = BeautifulSoup(page_source, 'html.parser')
        find_all_foto = soup.find_all('img')
        return find_all_foto
    except Exception as e:
        print("Не вдалося знайти зображення:", e)
        return None
    
def download_images(fotos, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for index, foto in enumerate(fotos):
        img_url = foto.get('src')
        if img_url:
            try:
                img_data = requests.get(img_url).content
                with open(f"{folder}/image_{index + 1}.jpg", 'wb') as handler:
                    handler.write(img_data)
                print(f"Image {index + 1} downloaded: {img_url}")
                print('\n')
            except Exception as e:
                print(f"Could not download image {img_url}: {e}")
    



def main():
    try:
        driver.get('https://www.instagram.com/')
        username_to_search = search_user()
        time.sleep(random.randrange(2, 5))

        login(username, password)
        time.sleep(random.randrange(2, 5))

        search(username_to_search)
        page_source = get_page_source()
        fotos = get_all_fotos(page_source)
        
        if fotos:
            download_images(fotos, folder=username_to_search)
            
                
        
        time.sleep(random.randrange(2, 5))
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    main()
