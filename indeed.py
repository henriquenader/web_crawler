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

def get_data_from_page(driver):
    element = driver.find_element(By.CLASS_NAME, value='jobsearch-LeftPane')
    html = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html, "html.parser")

    # LINKS
    links = []
    li = soup.find_all('li')
    for i, el in enumerate(li):
        if i % 2 == 0:
            try:
                link = 'indeed.de' + el.find_all('a')[0]['href']
                links.append({"Link": link})
            except:
                pass
    df_links = pd.DataFrame(links)

    # TITLES
    title = driver.find_elements(By.TAG_NAME, value='h2')
    titles = []
    for t in title:
        t = t.get_attribute('innerHTML')
        soup = BeautifulSoup(t, "html.parser")
        title = soup.get_text()
        titles.append({"Title": title})
    df_titles = pd.DataFrame(titles)

    # COMPANIES
    company = driver.find_elements(By.CLASS_NAME, value='companyName')
    companies = []
    for c in company:
        c = c.get_attribute('innerHTML')
        soup = BeautifulSoup(c, "html.parser")
        company = soup.get_text()
        companies.append({"Company": company})
    df_companies = pd.DataFrame(companies)

    # LOCATIONS
    location = driver.find_elements(By.CLASS_NAME, value='companyLocation')
    locations = []
    for l in location:
        l = l.get_attribute('innerHTML')
        soup = BeautifulSoup(l, "html.parser")
        location = soup.get_text()
        locations.append({"Location": location})
    df_locations = pd.DataFrame(locations)

    # POSTED
    posted = driver.find_elements(By.CLASS_NAME, value='date')
    posteds = []
    for p in posted:
        p = p.get_attribute('innerHTML')
        soup = BeautifulSoup(p, "html.parser")
        posted = soup.get_text()
        posteds.append({"Date": posted})
    df_posteds = pd.DataFrame(posteds)

    # DESCRIPTION
    description = driver.find_elements(By.CLASS_NAME, value='job-snippet')
    descriptions = []
    for d in description:
        d = d.get_attribute('innerHTML')
        soup = BeautifulSoup(d, "html.parser")
        description = soup.get_text()
        descriptions.append({"Description": description})
    df_descriptions = pd.DataFrame(descriptions)

    # Combine and clean the DataFrame
    df = pd.concat([df_titles, df_companies, df_locations, df_posteds, df_descriptions, df_links], axis=1)
    df = df.dropna()

    return df

def get_indeed(skill, city):
    options = Options()
    # options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(f"https://de.indeed.com/jobs?q={skill}&l={city}&from=searchOnHP")

    time.sleep(10)

    cookies = driver.find_element(By.ID, value='onetrust-accept-btn-handler')
    cookies.click()
    time.sleep(5)

    # Get the data from the first page
    first_page_df = get_data_from_page(driver)

    all_dfs = [first_page_df]

    index = 2
    while True:
        try:
            css_selector = f'[data-testid="pagination-page-{index}"]'
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            wait = WebDriverWait(driver, 10)
            pagination = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
            driver.execute_script("arguments[0].scrollIntoView();", pagination)
            action = webdriver.ActionChains(driver)
            action.move_to_element(pagination).click().perform()




            time.sleep(2)
            # try:
            #     x_button = driver.find_element(By.XPATH, value='//*[@id="mosaic-modal-mosaic-provider-desktopserp-jobalert-popup"]/div/div/div[1]/div/button')
            # except:
            #     pass

            # Perform any other actions you want after clicking the pagination element

            # Get the data from the current page
            current_page_df = get_data_from_page(driver)
            all_dfs.append(current_page_df)

            # Allow the page to load before looking for the next element
            time.sleep(2)

            if index == 11:
                break

            index += 1
        except NoSuchElementException:
            # Break the loop when no more pagination elements are found
            break

    # Combine all DataFrames into a single DataFrame
    final_df = pd.concat(all_dfs, ignore_index=True)

    return final_df

