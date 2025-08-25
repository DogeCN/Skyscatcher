from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException
from traceback import format_exception_only
import time


try:
    try:
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Edge()
    while True:
        try:
            url = "https://tieba.baidu.com"
            driver.get(url)
            while True:
                time.sleep(1)
                curl = driver.current_url
                if "/p/" in curl:
                    parts = curl.split("/p/")
                    if len(parts) > 1:
                        id = parts[1].split("?")[0]
                        if id.isdigit():
                            for c in driver.get_cookies():
                                if c["name"] == "BDUSS":
                                    break
                            else:
                                continue
                            url += f"/p/{id}?see_lz=1"
                            break
            stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            with open(stamp + ".html", "w", encoding="utf-8") as f:
                total = None
                page = 1
                while True:
                    driver.get(url + f"&pn={page}")
                    if not total:
                        title = driver.title
                        f.write(
                            f"<html><head><title>{title}</title></head><body><h1>{title}</h1>"
                        )
                        try:
                            f.write(
                                f"<h2>Author: {driver.find_element(
                                By.CLASS_NAME, "p_author_name"
                            ).text.strip()}</h2>"
                            )
                        except:
                            pass
                        total = int(
                            driver.find_element(By.CSS_SELECTOR, "li.l_reply_num")
                            .find_elements(By.TAG_NAME, "span")[-1]
                            .text
                        )
                    post_divs = driver.find_elements(
                        By.CSS_SELECTOR, "div.l_post.l_post_bright.j_l_post.clearfix"
                    )
                    for div in post_divs:
                        try:
                            f.write(
                                div.find_element(
                                    By.CLASS_NAME, "d_post_content"
                                ).get_attribute("outerHTML")
                                + "<br><br>"
                            )
                        except:
                            continue
                    if page >= total:
                        break
                    page += 1
                f.write("</body></html>")
        except NoSuchWindowException:
            break
except Exception as e:
    open(f"Error.txt", "w", encoding="utf-8").writelines(format_exception_only(e))
