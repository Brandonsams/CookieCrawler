from multiprocessing import set_forkserver_preload
import requests
from bs4 import BeautifulSoup as bs
import shutil
import datetime
import pandas as pd
import collections


class CookieJar:
    cookie_csv_filename = "cookies.csv"

    def __init__(self, cookie_jar_dir="./cookie_jar"):
        self.cookie_jar_dir = cookie_jar_dir
        self.cookie_collection = []
        # self.load_old_cookies()

    def add_cookie(self, new_cookie):
        self.cookie_collection.append(new_cookie)

    def load_old_cookies(self):
        df = pd.read_csv(
            filepath=f"{self.cookie_jar_dir}/{CookieJar.cookie_csv_filename}", index_col="id")
        old_cookies = [(Cookie(row.HourOfDay, row.Percentage))
                       for index, row in df.iterrows()]

    def save_to_cookie_jar_dir(self):
        df = pd.DataFrame([c.__dict__ for c in self.cookie_collection])
        df.to_csv(
            f"{self.cookie_jar_dir}/{CookieJar.cookie_csv_filename}", index_label="id")


class Cookie():
    def __init__(self, title, description, image_url):
        self.title = title
        self.description = description
        self.image_url = image_url
        self.image_filename = image_url.split("/")[-1]
        self.date = datetime.date.today()

    def save_cookie_image(self, dest_dir):
        out_path = f"{dest_dir}/{self.image_filename}"
        # Get request on full_url
        r = requests.get(self.image_url, stream=True)
        if r.status_code == 200:  # 200 status code = OK
            with open(out_path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            
    @classmethod
    def from_df_row(self, df_row):
        # TODO: Finish this part
         Reading(row.HourOfDay,row.Percentage)) for index, row in df.iterrows() ]

    # def __repr__(self):
    #     return f'{self.__class__.__name__}> (title {self.title}, description {self.description}, image_url {self.image_url}, image_filename {self.image_filename}, date {self.date})'

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
            cookies.append(
                Cookie(title=title, description=description, image_url=image_url))
        return cookies
