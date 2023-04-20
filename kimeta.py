import json
import numpy as np
import pandas as pd
import pandas as pd
import re
import streamlit as st
import streamlit as st
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def clean_span(li):
    span = li.find('span')
    neu = span.find('span')
    if neu:
        neu.extract()
    return span


def get_kimeta(skill, city, radius):

    options = Options()
    options.headless = False

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    url = f"https://www.kimeta.de/search?q={skill}&loc={city}&r={radius}"
    driver.get(url)
    # create an f string and change skill and city to variables

    page = 1
    while True:
        try:
            more_button = driver.find_element(By.CSS_SELECTOR, f"a[href='/search?q={skill}&loc={city}&r={radius}&page={page}']")
            more_button.click()
            time.sleep(2)
            page += 1
        except:
            break
    
    
    element = driver.find_element(
        By.XPATH, value='//*[@id="__next"]/div/div[2]/div[1]/div[1]/ul[1]')
    element2 = driver.find_element(
        By.XPATH, value='//*[@id="__next"]/div/div[2]/div[1]/div[1]/ul[2]')
    html2 = element2.get_attribute('innerHTML')
    html = element.get_attribute('innerHTML')
    soup2 = BeautifulSoup(html2, "html.parser")
    soup = BeautifulSoup(html, "html.parser")

    links_kimeta = []
    for i in soup.find_all('a', href=True):
        if '/search' in i['href']:
            links_kimeta.append(
                {
                    "Link": 'http://kimeta.de' + i['href'],
                }
            )

    links_kimeta2 = []
    for i2 in soup2.find_all('a', href=True):
        if '/search' in i2['href']:
            links_kimeta2.append(
                {
                    "Link": 'http://kimeta.de' + i2['href'],
                }
            )

    df_link_kimeta = pd.DataFrame(links_kimeta)
    df_link_kimeta2 = pd.DataFrame(links_kimeta2)
    df_link_kimeta = pd.concat([df_link_kimeta, df_link_kimeta2], axis=0)

    jobs_name = []
    for i in soup.find_all('h3'):
        title = i.text
        title = title.strip()
        jobs_name.append(
            {
                "Title": title,
            }
        )

    df_jobs_name_kimeta = pd.DataFrame(jobs_name)

    jobs_name2 = []
    for i2 in soup2.find_all('h3'):
        title2 = i2.text
        title2 = title2.strip()
        jobs_name2.append(
            {
                "Title": title2,
            }
        )
    df_jobs_name_kimeta2 = pd.DataFrame(jobs_name2)
    df_jobs_name_kimeta = pd.concat(
        [df_jobs_name_kimeta, df_jobs_name_kimeta2], axis=0)

    company_name = []

    for i in soup.find_all('li'):
        company = clean_span(i).text
        company = company.strip()
        company_name.append(
            {
                "Company": company,
            }
        )

    df_company = pd.DataFrame(company_name)

    company_name2 = []
    for i2 in soup2.find_all('li'):
        company2 = clean_span(i2).text
        company2 = company2.strip()
        company_name2.append(
            {
                "Company": company2,
            }
        )

    df_company2 = pd.DataFrame(company_name2)
    df_company = pd.concat([df_company, df_company2], axis=0)

    locations = []
    for i in soup.find_all(attrs={'class': 'locationtext'}):
        location = i.text
        location = location.strip()
        locations.append(
            {
                "Location": location,
            }
        )
    df_location = pd.DataFrame(locations)

    locations2 = []
    for i2 in soup2.find_all(attrs={'class': 'locationtext'}):
        location2 = i2.text
        location2 = location2.strip()
        locations2.append(
            {
                "Location": location2,
            }
        )
    df_location2 = pd.DataFrame(locations2)
    df_location = pd.concat([df_location, df_location2], axis=0)

    return pd.concat([df_jobs_name_kimeta, df_company, df_location, df_link_kimeta], axis=1)

