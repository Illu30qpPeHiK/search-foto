import os
import requests
import logging

class ImageDownloader:
    def __init__(self, folder):
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

    def download_images(self, site_name, image_urls):
        folder_path = os.path.join(self.folder, site_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for index, img_url in enumerate(image_urls):
            if img_url:
                try:
                    img_data = requests.get(img_url).content
                    with open(f"{folder_path}/image_{index + 1}.jpg", 'wb') as handler:
                        handler.write(img_data)
                    logging.info(f"Image {index + 1} downloaded from {site_name}: {img_url}")
                except Exception as e:
                    logging.error(f"Could not download image {img_url} from {site_name}: {e}")