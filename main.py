import crumbl

cookie_jar = crumbl.CookieJar()

cc = crumbl.CookieCrawler()
cookies = cc.find_cookies()
for cookie in cookies:
    cookie.save_cookie_image("./cookie_jar/images")
    cookie_jar.add_cookie(cookie)

cookie_jar.save_to_cookie_jar_dir()