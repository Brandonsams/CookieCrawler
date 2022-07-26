import crumbl

cookie_jar = crumbl.CookieJar()
cookie_jar.delete_all_cookies()
cookie_jar.delete_all_cookie_images()
cookie_jar.save_to_cookie_jar_dir()