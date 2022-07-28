import crumbl

# Storage
cookie_jar = crumbl.CookieJar()

# Web Crawler
cc = crumbl.CookieCrawler()
cookies = cc.find_cookies()

# Save the Data
cookie_jar.add_cookies(cookies)
cookie_jar.save_cookie_jar()


# [cookie.save_cookie_image("./cookie_jar/images") for cookie in cookie_jar.cookie_collection]