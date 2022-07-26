import requests
from bs4 import BeautifulSoup as bs
import shutil
import datetime
import pandas as pd
import collections
import os
import base64

class CookieJar:
    cookie_csv_filename = "cookies.csv"

    def __init__(self, cookie_jar_dir="./cookie_jar"):
        self.cookie_jar_dir = cookie_jar_dir
        self.images_dir = f"{self.cookie_jar_dir}/images"
        self.cookie_collection = []
        self.load_old_cookies()

    def add_cookies(self, new_cookies):
        for new_cookie in new_cookies:
            self.add_cookie(new_cookie)

    def add_cookie(self, new_cookie):
        self.cookie_collection.append(new_cookie)
        new_cookie.save_cookie_image(self.images_dir)

    def load_old_cookies(self):
        df = pd.read_csv(f"{self.cookie_jar_dir}/{CookieJar.cookie_csv_filename}",index_col="id")
        self.cookie_collection = [Cookie.from_df_row(row) for index, row in df.iterrows()]

    def save_to_cookie_jar_dir(self):
        df = pd.DataFrame([c.__dict__ for c in self.cookie_collection])
        df.to_csv(
            f"{self.cookie_jar_dir}/{CookieJar.cookie_csv_filename}", index_label="id")

    def archive_cookies(self):
        pass

    def delete_all_cookies(self):
        self.cookie_collection.clear()

    def delete_all_cookie_images(self):
        shutil.rmtree(self.images_dir)
        os.mkdir(self.images_dir)

class Cookie:
    def __init__(self, title, description, image_url):
        self.date = datetime.date.today()
        self.title = title
        self.description = description
        self.image_url = image_url
        self.image_filename = image_url.split("/")[-1]
        response = requests.get(image_url)
        if r.status_code == 200:  # 200 status code = OK
            self.image_base64 = base64.b64encode(response.content)
        else:
            self.image_base64 = None

    def save_cookie_image(self, dest_dir):
        imgdata = base64.b64decode(self.image_base64)
        outfile_path = f"{dest_dir}/{self.image_filename}"
        with open(outfile_path, 'wb') as f:
            f.write(imgdata)

    @classmethod
    def from_df_row(cls, df_row):
        title = df_row.title
        description = df_row.description
        image_url = df_row.image_url
        return Cookie(title, description, image_url)

    def __str__(self):
        return f"{self.title} | {self.description}"


class CookieCrawler:
    def __init__(self, crumbl_url="https://crumblcookies.com"):
        self.crumbl_url = crumbl_url

    def find_cookies(self):
        resp = requests.get(self.crumbl_url)
        soup = bs(resp.content, "html.parser")
        flavors = soup.find(id="weekly-cookie-flavors")
        cookies = []
        for flavor in flavors:
            title = flavor.find("h3").text
            description = flavor.find("p").text
            image_url = ""
            for img in flavor.find_all("img"):
                if "crumbl.video" in img["src"]:
                    if img["src"].endswith(".png"):
                        image_url = img["src"]
            cookies.append(Cookie(title=title, description=description, image_url=image_url))
        return cookies
