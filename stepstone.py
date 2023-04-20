import json
import numpy as np
import pandas as pd
import re
import streamlit as st
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

from selenium.common.exceptions import NoSuchElementException

def get_stepstone(skill, city, radius, num_pages=10):
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    all_data = pd.DataFrame()

    for page in range(1, num_pages + 1):
        driver.get(f"https://www.stepstone.de/jobs/{skill}/in-{city}?radius={radius}&rsearch=1&page={page}")

        time.sleep(6)

        try:
            element = driver.find_element(By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[2]/div[2]/div')
            html = element.get_attribute('innerHTML')
            soup = BeautifulSoup(html, "html.parser")

            ar = soup.find_all('a')
            links = []
            for so in soup.find_all('a', href=True):
                if '/stelle' in so['href']:
                    links.append(
                        {
                            "Link": 'http://stepstone.de' + so['href'],
                        }
                    )

            titles = []
            t = soup.find_all('a')
            for i in t:
                title = i.text
                titles.append(
                    {
                        "Title": title,
                    }
                )

            df1 = pd.DataFrame(titles)
            df1 = df1[df1.Title != '']

            comp = []
            for s in soup.find_all(attrs={"data-at": "job-item-company-name"}):
                s = s.get_text()
                comp.append(
                    {
                        "Company": s,
                    }
                )

            locat = []
            for l in soup.find_all(attrs={"data-at": "job-item-location"}):
                l = l.get_text()
                locat.append(
                    {
                        "Location": l,
                    }
                )

            post = []
            for l in soup.find_all(attrs={"data-at": "job-item-timeago"}):
                l = l.get_text()
                post.append(
                    {
                        "Date": l,
                    }
                )

            df3 = pd.DataFrame(comp)
            df4 = pd.DataFrame(locat)
            df5 = pd.DataFrame(post)
            
            df6 = pd.DataFrame(links)
        
            
            # ...

            # Concatenate the DataFrames
            df1 = pd.concat([df1, df3, df4, df5, df6], axis=1)
            df1 = df1.dropna()

            # Append the DataFrame for the current page to the all_data DataFrame
            all_data = all_data.append(df1, ignore_index=True)

        except NoSuchElementException:
            print(f"Element not found on page {page}. Skipping this page...")


    return all_data
