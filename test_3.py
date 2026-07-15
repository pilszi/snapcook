from db import connect
import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

"""
    #__next > div > main > div.token__Component-sc-1o2h3sm-0.jjTxDH > div:nth-child(4) > div > ul > li > ul > li > div > div
"""

"""
    #__next > div > main > div.token__Component-sc-1o2h3sm-0.jjTxDH > div:nth-child(5) > div > div:nth-child(1) > div:nth-child(2) > p
"""

conn = connect()
sql = """ 
    SELECT link FROM recipe_link
"""
df = pd.read_sql(sql, conn)
# print(df.head())
for url in df.head(1)['LINK']:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.select_one("h2") or soup.select_one(".RecipeDetailstyle__Title-q7sykd-4 kIVrZW")
    # print(title.text)
    ingredient = soup.select("#__next > div > main > div.token__Component-sc-1o2h3sm-0.jjTxDH > div:nth-child(4) > div > ul > li > ul > li > div > div")
    # for ing in ingredient:
        # print(ing.text)
    recipes = soup.select("#__next > div > main > div.token__Component-sc-1o2h3sm-0.jjTxDH > div:nth-child(5) > div > div")
    print(recipes)
    print(len(recipes))
    


