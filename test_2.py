from bs4 import BeautifulSoup
from starlette.responses import RedirectResponse
from selenium import webdriver
import requests
import time
from db import connect

url = "https://wtable.co.kr/recipes"

selector = """
    #__next div main div div div section section div a
"""
"""
    #__next > div > main > div.token__Component-sc-1o2h3sm-0.jjTxDH > section > div.RecipeDetailstyle__MetaHeader-q7sykd-1.jyPkMJ > div > h2
"""

browser = webdriver.Chrome()
browser.get(url)
browser.maximize_window()

browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

term = 2

prev_height = browser.execute_script("return document.body.scrollHeight")
link_elems = []
while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        elements = soup.select(selector)
        # print(len(elements))
        for elem in elements:
            link = elem.get("href")
            link = link.replace("/recipes", "")
            recipe_link = url + link
            link_elems.append(recipe_link)

    else : 
        print(response.status_code)
    time.sleep(term)

    curr_height = browser.execute_script("return document.body.scrollHeight")
    if curr_height == prev_height:
        break
    prev_height = curr_height
# print(len(link_elems))

conn = connect()

sql = """
    INSERT INTO recipe_link(id, link) VALUES(recipe_link_seq.NEXTVAL, :1)
"""
with conn.cursor() as cur:
    for link in link_elems:
        cur.execute(sql, [link])
conn.commit()


