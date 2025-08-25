from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSessionIdException, NoSuchWindowException
from traceback import format_exception_only
import time

STYLE = """<style>body {max-width:700px;margin:40pxauto;background:#f6f8fa;color:#222;font-family:"SegoeUI","HelveticaNeue",Arial,"PingFangSC","MicrosoftYaHei",sans-serif;font-size:1.15em;line-height:1.8;box-shadow:0016px#ccc;border-radius:12px;padding:32px32px32px32px;transition:background0.3s,color0.3s;}h1,h2{text-align:center;font-weight:600;}img{max-width:100%;border-radius:6px;box-shadow:02px8px#2222;margin:12px0;display:block;margin-left:auto;margin-right:auto;}@media(prefers-color-scheme:dark){body{background:#181a20;color:#e2e2e2;box-shadow:0016px#222;}img{box-shadow:02px8px#0008;}}</style>"""
INTERRUPT = InvalidSessionIdException | NoSuchWindowException

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
                            f"<html><head><title>{title}</title>{STYLE}</head><body><h1>{title}</h1>"
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
                                div.find_element(By.CLASS_NAME, "d_post_content")
                                .get_attribute("innerHTML")
                                .strip(
                                    """<div class="replace_tip" style="width: 558px;"><i class="icon-expand"></i>点击展开，查看完整图片</div>"""
                                )
                                + "<br><br>"
                            )
                        except:
                            continue
                    if page >= total:
                        break
                    page += 1
                f.write("</body></html>")
        except INTERRUPT:
            break
except Exception as e:
    open(f"Error.txt", "w", encoding="utf-8").writelines(format_exception_only(e))
