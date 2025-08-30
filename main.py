from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from traceback import format_exception_only
import time

OPT = (
    "prefs",
    {"download.prompt_for_download": True, "download.directory_upgrade": True},
)
STYLE = "<style>body{background:#1e1e1e;color:#c0c0c0;font-family:Arial,sans-serif;font-size:1.6em;padding:60px 10%}p{margin:1.2em 0}.q{width:30px;height:30px}.lz{width:30%;height:auto;border-radius:6px;transition:transform 200ms ease;transform-origin:center center;cursor:pointer}.lz.large{width:100%}.lz:hover{opacity:0.9}.ct{text-align:center;margin:12px auto;transition:margin 200ms ease}</style><script>function enlarge(img){img.classList.toggle('large');adjustLayout();}function rotate(img,event){event.preventDefault();const rotation=parseInt(img.dataset.rotation||'0')+90;img.dataset.rotation=rotation;img.style.transform=`rotate(${rotation}deg)`;adjustLayout();return false;}function adjustLayout(){const containers=document.querySelectorAll('.ct');containers.forEach(container=>{const img=container.querySelector('.lz');const rotation=parseInt(img.dataset.rotation||'0')%180;if(rotation!==0){container.style.margin=`${(img.offsetWidth-img.offsetHeight)*0.5+12}px auto`;}else{container.style.margin='12px auto';}});}</script>"
PROC = r"""return '<p>'+arguments[0].innerHTML.replace(/<div[^>]*replace_tip[^>]*>.*?<\/div>/g,'').replace(/<div[^>]*>/g,'').replace(/<\/div>/g,'').replace(/<img[^>]*>/g,m=>{let src=m.match(/src="[^"]*"/);return m.includes('BDE_Smiley')?`<img class="q" ${src?src[0]:''}>`:src?`<div class="ct"><img class="lz" ${src[0]} onclick="enlarge(this)" oncontextmenu="rotate(this,event)"></div>`:m;}).replace(/<a[^>]*portrait="([^"]*)"[^>]*>([^<]*)<\/a>/g,'<a href="https://tieba.baidu.com/home/main?id=$1">$2</a>').replace(/\s+/g,' ').replace(/> </g,'><')+'</p>';"""
BLOB = "var blob=new Blob([arguments[0]],{type:'text/html'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=arguments[1];document.body.appendChild(a);a.click();document.body.removeChild(a);"

try:
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option(*OPT)
        driver = webdriver.Chrome(options)
    except:
        options = webdriver.EdgeOptions()
        options.add_experimental_option(*OPT)
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
                    cache += f"<html><head><title>{title}</title>{STYLE}</head><body><h1>{title}</h1>"
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
                    cache += driver.execute_script(
                        PROC,
                        div.find_element(By.CLASS_NAME, "d_post_content"),
                    )
                if page >= total:
                    break
                page += 1
            cache += "</body></html>"
            driver.execute_script(
                BLOB,
                cache,
                f"{time.strftime('Skyscatcher_%Y%m%d_%H%M%S', time.localtime())}.html",
            )
        except WebDriverException:
            driver.quit()
            break
except Exception as e:
    open(f"Error.txt", "w", encoding="utf-8").writelines(format_exception_only(e))
