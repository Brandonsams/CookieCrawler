import requests
from bs4 import BeautifulSoup as bs
import shutil


class Cookie:
    def __init__(self, title, description, image_url):
        self.title = title
        self.description = description
        self.image_url = image_url

    def save_cookie_image(self, dest_dir):
        filename = self.image_url.split("/")[-1]
        out_path = f"{dest_dir}/{filename}"
        # Get request on full_url
        r = requests.get(self.image_url, stream=True)
        if r.status_code == 200:  # 200 status code = OK
            with open(out_path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

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
