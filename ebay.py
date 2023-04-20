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

def get_ebay():
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(
        f"https://www.linkedin.com/jobs/ebay-kleinanzeigen-jobs-worldwide/?currentJobId=3430341588&f_C=18223802")
    # create an f string and change skill and city to variables

    time.sleep(5)

    element = driver.find_element(
        By.XPATH, value='//*[@id="main-content"]/section[2]')
    html = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html, "html.parser")

    y = soup.find_all('a')
    links_ebay = []
    for i in soup.find_all('a', href=True):
        if 'https://' in i['href']:
            links_ebay.append(
                {
                    "Link": i['href'],
                }
            )

    df_link_ebay = pd.DataFrame(links_ebay)

    jobs_name = []
    for i in soup.find_all(attrs={"data-tracking-control-name": "public_jobs_jserp-result_search-card"}):
        title = i.text
        title = title.strip()
        jobs_name.append(
            {
                "Title": title,
            }
        )

    df_jobs_name_ebay = pd.DataFrame(jobs_name)

    company_name = []
    for i in soup.find_all(attrs={"data-tracking-control-name": "public_jobs_jserp-result_job-search-card-subtitle"}):
        company = i.text
        company = company.strip()
        company_name.append(
            {
                "Company": company,
            }
        )
    df_company = pd.DataFrame(company_name)

    location_name = []
    for i in soup.find_all(attrs={'class': 'job-search-card__location'}):
        location = i.text
        # location = location.strip()
        location_name.append(
            {
                "Location": location,
            }
        )

    df_location = pd.DataFrame(location_name)
    # df_location

    date_posted = []
    for i in soup.find_all(attrs={'class': 'job-search-card__listdate'}):
        date = i.text
        date = date.strip()
        date_posted.append(
            {
                "Date": date,
            }
        )
    df_posted = pd.DataFrame(date_posted)

    df_ebay = pd.concat([df_jobs_name_ebay, df_company,
                        df_location, df_posted, df_link_ebay], axis=1)
    df_ebay = df_ebay.dropna()

    return df_ebay