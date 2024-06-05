import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
from PIL import Image
import time
import random
import requests
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

    password_input = driver.find_element(By.NAME, 'password')
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
            for foto in fotos:
                print(foto.get('src'))
                print('\n')
                
        
        time.sleep(random.randrange(15, 30))
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    main()
