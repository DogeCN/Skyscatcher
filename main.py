from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    InvalidSessionIdException,
    NoSuchWindowException,
    WebDriverException,
)
from traceback import format_exception_only
import time

blob_js = """var content=`%s`;var filename="%s";var blob=new Blob([content],{type:"text/html"});var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=filename;document.body.appendChild(a);a.click();document.body.removeChild(a);"""

try:
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs",
            {
                "download.prompt_for_download": True,
                "download.directory_upgrade": True,
            },
        )
        driver = webdriver.Chrome(options)
    except:
        options = webdriver.EdgeOptions()
        options.add_experimental_option(
            "prefs",
            {
                "download.prompt_for_download": True,
                "download.directory_upgrade": True,
            },
        )
        driver = webdriver.Edge(options)
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
            cache = ""
            total = None
            page = 1
            while True:
                driver.get(url + f"&pn={page}")
                if not total:
                    title = driver.find_element(
                        By.CLASS_NAME, "core_title_txt"
                    ).text.strip()
                    style = """<style>body{margin:0;background:#1e1e1e;color:#c0c0c0;font-family:"SegoeUI","HelveticaNeue",Arial,"PingFangSC","MicrosoftYaHei",sans-serif;font-size:1.6em;line-height:2.1;padding:60px 8%;min-height:100vh;}h1,h2{text-align:left;font-weight:400;margin:2em 0 1em 0;font-size:1.6em;}h1{font-size:2.2em;margin-top:1em;}p{margin:1.2em 0;text-align:justify;}.lz{max-width:100%;border-radius:6px;box-shadow:0 2px 8px #2222;margin:12px 0;display:block;margin-left:auto;margin-right:auto;}</style>"""
                    cache += f"<html><head><title>{title}</title>{style}</head><body><h1>{title}</h1>"
                    try:
                        cache += f"<h2>Author: {driver.find_element(
                            By.CLASS_NAME, "p_author_name"
                        ).text.strip()}</h2>"
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
                        content_element = div.find_element(
                            By.CLASS_NAME, "d_post_content"
                        )
                        nodes = driver.execute_script(
                            "return Array.from(arguments[0].childNodes).map(n => ({type: n.nodeType, name: n.nodeName, value: n.nodeValue, src: n.src || ''}));",
                            content_element,
                        )
                        for node in nodes:
                            if node["type"] == 3:
                                text = node["value"]
                                if text:
                                    cache += text
                            elif node["type"] == 1 and node["name"] == "IMG":
                                img_url = node["src"]
                                if img_url:
                                    cache += '<img src="%s"%s/>' % (
                                        img_url,
                                        ('class="lz"' if "forum" in img_url else ""),
                                    )
                        cache += "<br><br>"
                    except:
                        continue
                if page >= total:
                    break
                page += 1
            cache += "</body></html>"
            driver.execute_script(
                blob_js
                % (
                    cache,
                    f"{time.strftime('Skyscatcher_%Y%m%d_%H%M%S', time.localtime())}.html",
                )
            )
        except (
            InvalidSessionIdException,
            NoSuchWindowException,
            WebDriverException,
            TypeError,
        ):
            break
except Exception as e:
    open(f"Error.txt", "w", encoding="utf-8").writelines(format_exception_only(e))
