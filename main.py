import crumbl

cc = crumbl.CookieCrawler()
cookies = cc.find_cookies()
for cookie in cookies:
    cookie.save_cookie_image("./img")