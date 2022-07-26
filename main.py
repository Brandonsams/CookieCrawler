import crumbl

# Storage
cookie_jar = crumbl.CookieJar()

# Web Crawler
cc = crumbl.CookieCrawler()
cookies = cc.find_cookies()

# Save the Data
cookie_jar.add_cookies(cookies)
cookie_jar.save_to_cookie_jar_dir()

cookies[0].save_cookie_image_2("./")