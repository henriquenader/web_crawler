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


def get_jobware(skill, city, radius):

    options = Options()
    options.headless = False
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    url = f"https://www.jobware.de/jobsuche?jw_jobname={skill}&jw_jobort={city}&jw_ort_distance={radius}"

    
    driver.get(url)

    time.sleep(2)

    # get element by text inside it
    button = driver.find_element(By.XPATH, '//button[.//text()="Alle akzeptieren"]')

    button.click()

    while True:
        time.sleep(2)
        try:
            try:
                close = driver.find_element(
                    By.XPATH, value='//*[@id="mat-dialog-0"]/div/button/span[1]/mat-icon')
                close.click()
            except:
                pass

            page_button = driver.find_element(By.XPATH, "//button[@title='Weitere Jobs laden']")
            page_button.click()
        except:
            break

    time.sleep(5)

    element = driver.find_element(
        By.XPATH, value='/html/body/jw-83hzo/section/main/div[2]/div/div[2]/div')
    html = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html, "html.parser")

    # Initialize an empty DataFrame
    all_data = pd.DataFrame()

    job_titles = []
    for i in soup.find_all('h2'):
        title = i.text
        title = title.strip()
        job_titles.append(
            {
                "Title": title,
            }
        )
    df_titles_jobware = pd.DataFrame(job_titles)

    company_names = []
    for i in soup.find_all(attrs={'class': 'company'}):
        company = i.text
        company = company.strip()
        company_names.append(
            {
                "Company": company,
            }
        )
    df_company_jobware = pd.DataFrame(company_names)

    locations = []
    for i in soup.find_all(attrs={'class': 'location'}):
        location = i.text
        location = location.strip()
        locations.append(
            {
                "Location": location,
            }
        )
    df_location_jobware = pd.DataFrame(locations)

    descriptions = []
    for i in soup.find_all(attrs={'class': 'task'}):
        description = i.text
        description = description.strip()
        descriptions.append(
            {
                "Description": description,
            }
        )
    df_description_jobware = pd.DataFrame(descriptions)

    dates = []
    for i in soup.find_all(attrs={'class': 'date'}):
        date = i.text
        date = date.strip()
        dates.append(
            {
                "Date": date,
            }
        )
    df_date_jobware = pd.DataFrame(dates)

    links = []
    a = soup.find_all('a')
    for i in a:
        a = i.get('href')
        links.append(
            {
                "Link": 'http://jobware.de' + a,
            }
        )
    df_link_jobware = pd.DataFrame(links)

    df_jobware = pd.concat([df_titles_jobware, df_company_jobware, df_location_jobware,
                            df_description_jobware, df_date_jobware, df_link_jobware], axis=1)
    df_jobware = df_jobware.dropna()

    # Append the DataFrame for the current page to the all_data DataFrame
    all_data = all_data.append(df_jobware, ignore_index=True)


    return df_jobware