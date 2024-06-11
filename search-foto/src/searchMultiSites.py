import os
import time
import random
import logging
from searchData import SearchData
from imageDownloader import ImageDownloader

logging.basicConfig(level=logging.INFO)

class SearchMultiSites:
    def __init__(self, sites, username_to_search, login_required, username, password):
        self.sites = sites
        self.username_to_search = username_to_search
        self.login_required = login_required
        self.username = username
        self.password = password

    def search_on_multiple_sites(self):
        bot = SearchData(self.username, self.password)

        for site_url in self.sites:
            logging.info(f"Пошук на {site_url}")
            if self.login_required:
                bot.login(site_url)
                bot.search_user(self.username_to_search, site_url)
                image_urls = bot.scroll_and_collect_images()
                if not image_urls:
                    logging.warning("На першій спробі зображення не знайдені. Повторна спроба...")
                    bot.search_user(self.username_to_search, site_url)
                    image_urls = bot.scroll_and_collect_images()
            else:
                bot.search_user(self.username_to_search, site_url)
                image_urls = bot.scroll_and_collect_images()
                if not image_urls:
                    logging.warning("На першій спробі зображення не знайдені. Повторна спроба...")
                    bot.search_user(self.username_to_search, site_url)
                    image_urls = bot.scroll_and_collect_images()

            if image_urls:
                site_name = site_url.split('//')[1].split('/')[0]
                downloader = ImageDownloader(folder=self.username_to_search)
                downloader.download_images(site_name, image_urls)
            else:
                logging.warning(f"Не знайдено зображень для {self.username_to_search} на {site_url}")

            time.sleep(random.uniform(2, 5))
        bot.close()
