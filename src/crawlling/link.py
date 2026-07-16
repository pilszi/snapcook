from bs4 import BeautifulSoup
from starlette.responses import RedirectResponse
from selenium import webdriver
import time
from db import connect


url = "https://wtable.co.kr/recipes"

browser = webdriver.Chrome()
browser.get(url)
browser.maximize_window()


term = 2
prev_height = browser.execute_script("return document.body.scrollHeight")
try:
    selector = "#__next div main div div div section section div a"
    link_elems = set()
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        time.sleep(term)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        elements = soup.select(selector)
        # print(len(elements))
        for elem in elements:
            link = elem.get("href")
            link = link.replace("/recipes", "")
            recipe_link = url + link
            link_elems.add(recipe_link)

        curr_height = browser.execute_script("return document.body.scrollHeight")
        if curr_height == prev_height:
            break
        prev_height = curr_height
    browser.quit()
    print(f'찾아낸 음식 : {len(link_elems)}개')


    sql = """
        INSERT INTO recipe_link(link) VALUES(:1)
    """
    try:
        conn = connect()
        cur = conn.cursor()
        with conn.cursor() as cur:
            for link in link_elems:
                cur.execute(sql, [link])
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"오류 발생으로 저장 건너뜀({link} : {e})")
except KeyError as k:
    print(f'잘 못 입력 하였습니다 : {k}')
except Exception as e:
    print(f'오류 발생으로 멈춤 : {e}')