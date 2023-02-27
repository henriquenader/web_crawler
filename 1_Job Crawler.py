import streamlit as st
import time
import numpy as np
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from urllib.error import URLError
import requests
import csv
import re
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

st.set_page_config(page_title="Job Crawler", page_icon="📈")

st.markdown("# Job Crawler")
st.sidebar.header("Job Crawler")
st.write(
    """This is an automated job crawler!"""
)


title1 = st.text_input('Search by Skill')
# st.write('The current movie title is', title)
location1 = st.text_input('Location')
# radius1 = st.text_input('Radius')
color = st.select_slider(
    'Select Radius',
    options=[10, 20, 30, 40, 50, 100])
# st.write('Selected Radius', color)



def get_ebay():

    options = Options()
    options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(f"https://www.linkedin.com/jobs/ebay-kleinanzeigen-jobs-worldwide/?currentJobId=3430341588&f_C=18223802")
    # create an f string and change skill and city to variables

    time.sleep(5)

    cookies = driver.find_element(By.XPATH, value='//*[@id="artdeco-global-alert-container"]/div/section/div/div[2]/button[1]')
    cookies.click()
    time.sleep(2)


    element = driver.find_element(By.XPATH, value='//*[@id="main-content"]/section[2]')
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
    # print(df_jobs_name_ebay)


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
    # print(df_company)

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
    # print(df_posted)


    df_ebay = pd.concat([df_jobs_name_ebay, df_company, df_location, df_posted, df_link_ebay], axis=1)
    df_ebay = df_ebay.dropna()

    return df_ebay



def get_indeed(skill, city):
    options = Options()
    # options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(f"https://de.indeed.com/jobs?q={skill}&l={city}&from=searchOnHP")
    # create an f string and change skill and city to variables

    time.sleep(10)

    cookies = driver.find_element(By.ID, value='onetrust-accept-btn-handler')
    cookies.click()
    time.sleep(5)

    element = driver.find_element(By.CLASS_NAME, value='jobsearch-LeftPane')
    html = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html, "html.parser")

    # LINKS
    ########################################

    links = []
    li = soup.find_all('li')
    for i, el in enumerate(li):
        #check if i is odd or even
        if i % 2 == 0:
            try:
                link = 'indeed.de' + el.find_all('a')[0]['href']
                links.append(
                        {
                            "Link": link,
                        }
                    )
            except:
                pass

    df_links = pd.DataFrame(links)

    #######################################

    # TITLES
    ########################################
    title = driver.find_elements(By.TAG_NAME, value='h2')
    titles = []
    for t in title:
        t = t.get_attribute('innerHTML')
        soup = BeautifulSoup(t, "html.parser")
        title = soup.get_text()
        # print(title)
        titles.append(
                {
                    "Title": title,
                }
            )

    df_titles = pd.DataFrame(titles)

    #######################################

    # COMPANIES
    ########################################
    company = driver.find_elements(By.CLASS_NAME, value='companyName')
    companies = []
    for c in company:
        c = c.get_attribute('innerHTML')
        soup = BeautifulSoup(c, "html.parser")
        company = soup.get_text()
        # print(company)
        companies.append(
                {
                    "Company": company,
                }
            )
    df_companies = pd.DataFrame(companies)

    #######################################

    # LOCATIONS
    ########################################

    location = driver.find_elements(By.CLASS_NAME, value='companyLocation')
    locations = []
    for l in location:
        l = l.get_attribute('innerHTML')
        soup = BeautifulSoup(l, "html.parser")
        location = soup.get_text()
        # print(location)
        locations.append(
                {
                    "Location": location,
                }
            )
    df_locations = pd.DataFrame(locations)

    #######################################

    # POSTED
    ########################################

    posted = driver.find_elements(By.CLASS_NAME, value='date')
    posteds = []
    for p in posted:
        p = p.get_attribute('innerHTML')
        soup = BeautifulSoup(p, "html.parser")
        posted = soup.get_text()
        # print(posted)
        posteds.append(
                {
                    "Date": posted,
                }
            )
    df_posteds = pd.DataFrame(posteds)

    #######################################

    # DESCRIPTION
    ########################################

    description = driver.find_elements(By.CLASS_NAME, value='job-snippet')
    descriptions = []
    for d in description:
        d = d.get_attribute('innerHTML')
        soup = BeautifulSoup(d, "html.parser")
        description = soup.get_text()
        # print(description)
        descriptions.append(
                {
                    "Description": description,
                }
            )
    df_descriptions = pd.DataFrame(descriptions)

    #######################################

    df = pd.concat([df_titles, df_companies, df_locations, df_posteds, df_descriptions, df_links], axis=1)
    df = df.dropna()

    return df




def get_stepstone(skill, city, radius):
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(f"https://www.stepstone.de/jobs/{skill}/in-{city}?radius={radius}&rsearch=1")
    # create an f string and change skill and city to variables

    time.sleep(6)

    element = driver.find_element(By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[2]/div[2]/div')
    html = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html, "html.parser")

    ar = soup.find_all('a') 
    links = []
    for so in soup.find_all('a', href=True):
        if '/stelle' in so['href']:
            links.append(
                    {
                        "Link": 'stepstone.de' + so['href'],
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

    df1 = pd.concat([df1, df3, df4, df5, df6], axis=1)
    df1 = df1.dropna()

    return df1



def clean_span(li):
    span = li.find('span')
    neu = span.find('span')
    if neu:
        neu.extract()
    return span

def get_kimeta(skill, city, radius):

        options = Options()
        options.headless = True

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(f"https://www.kimeta.de/search?q={skill}&loc={city}&r={radius}")
        # create an f string and change skill and city to variables

        time.sleep(6)

        element = driver.find_element(By.XPATH, value='//*[@id="__next"]/div/div[2]/div[1]/div[1]/ul[1]')
        element2 = driver.find_element(By.XPATH, value='//*[@id="__next"]/div/div[2]/div[1]/div[1]/ul[2]')
        html2 = element2.get_attribute('innerHTML')
        html = element.get_attribute('innerHTML')
        soup2 = BeautifulSoup(html2, "html.parser")
        soup = BeautifulSoup(html, "html.parser")

        j = soup.find_all('a')


        y = soup.find_all('a')
        links_kimeta = []
        for i in soup.find_all('a', href=True):
            if '/search' in i['href']:
                links_kimeta.append(
                        {
                            "Link": 'kimeta.de' + i['href'],
                            }
                        )

        j2 = soup2.find_all('a')


        y2 = soup2.find_all('a')
        links_kimeta2 = []
        for i2 in soup2.find_all('a', href=True):
            if '/search' in i2['href']:
                links_kimeta2.append(
                        {
                            "Link": 'kimeta.de' + i2['href'],
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
        df_jobs_name_kimeta = pd.concat([df_jobs_name_kimeta, df_jobs_name_kimeta2], axis=0)

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
        # print(df_company)


        locations = []
        for i in soup.find_all(attrs= {'class': 'locationtext'}):
            location = i.text
            location = location.strip()
            locations.append(
                    {
                        "Location": location,
                    }
                )
        df_location = pd.DataFrame(locations)

        locations2 = []
        for i2 in soup2.find_all(attrs= {'class': 'locationtext'}):
            location2 = i2.text
            location2 = location2.strip()
            locations2.append(
                    {
                        "Location": location2,
                    }
                )
        df_location2 = pd.DataFrame(locations2)
        df_location = pd.concat([df_location, df_location2], axis=0)

        df_kimeta = pd.concat([df_jobs_name_kimeta, df_company, df_location, df_link_kimeta], axis=1)
        return df_kimeta

def get_jobware(skill, city, radius):

    options = Options()
    options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(f"https://www.jobware.de/jobsuche?jw_jobname={skill}&jw_jobort={city}&jw_ort_distance={radius}")
    # create an f string and change skill and city to variables

    time.sleep(10)

    try:
        cookies = driver.find_element(By.XPATH, value='/html/body/div/div/div[3]/div[2]/button')
        cookies.click()
    except:
        pass

    time.sleep(5)

    try:
        close = driver.find_element(By.XPATH, value = '//*[@id="mat-dialog-0"]/div/button/span[1]/mat-icon')
        close.click()
    except:
        pass

    element = driver.find_element(By.XPATH, value='/html/body/jw-83hzo/section/main/div[2]/div/div[2]/div')
    html = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html, "html.parser")

    j = soup.find_all('a')
    
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
    for i in soup.find_all(attrs= {'class': 'company'}):
        company = i.text
        company = company.strip()
        company_names.append(
                {
                    "Company": company,
                }
            )
    df_company_jobware = pd.DataFrame(company_names)

    locations = []
    for i in soup.find_all(attrs= {'class': 'location'}):
        location = i.text
        location = location.strip()
        locations.append(
                {
                    "Location": location,
                }
            )
    df_location_jobware = pd.DataFrame(locations)

    descriptions = []
    for i in soup.find_all(attrs= {'class': 'task'}):
        description = i.text
        description = description.strip()
        descriptions.append(
                {
                    "Description": description,
                }
            )
    df_description_jobware = pd.DataFrame(descriptions)

    dates = []
    for i in soup.find_all(attrs= {'class': 'date'}):
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
                    "Link": 'jobware.de' + a,
                }
        )
    df_link_jobware = pd.DataFrame(links)

    df_jobware = pd.concat([df_titles_jobware, df_company_jobware, df_location_jobware, df_description_jobware, df_date_jobware, df_link_jobware], axis=1)
    df_jobware = df_jobware.dropna()

    return df_jobware


def convert_df(df):
# IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def main():

    if st.button('Run'):
        jobs_ebay = get_ebay()
        jobs_indeed = get_indeed(title1, location1)
        jobs_stepstone = get_stepstone(title1, location1, color)
        jobs_kimeta = get_kimeta(title1, location1, color)
        jobs_jobware = get_jobware(title1, location1, color)


    # if jobs_ebay:
    #     df_ebay = pd.DataFrame()
    #     for job in jobs_ebay:

    #         create_dict = {
    #             "Title": job["title"],
    #             "Company": job["company"],
    #             "Location": job["location"],
    #             "Posted": job["posted"],
    #             "Link": job["link"],
    #             "Description": job["description"],
    #         }
    #         df2 = pd.DataFrame(
    #             create_dict, index=[0])
    #         df_ebay = df_ebay.append(df2, ignore_index=True)

            
    # else:
    #     st.write("No results found.")

    # if jobs_indeed:
    #     df_indeed = pd.DataFrame()
    #     for job in jobs_indeed:

    #         create_dict = {
    #             "Title": job["title"],
    #             # "company": job["company"],
    #             "Location": job["location"],
    #             "Posted": job["posted"],
    #             "Link": job["link"],
    #             # "description": job["description"],
    #         }
    #         dff2 = pd.DataFrame(
    #             create_dict, index=[0])
    #         df_indeed = df_indeed.append(dff2, ignore_index=True)

            
    # else:
    #     st.write("No results found.")


    # if jobs_stepstone:
    #     df_stepstone = pd.DataFrame()
    #     for job in jobs_stepstone:

    #         create_dict = {
    #             "Title": job["title"],
    #             "Company": job["company"],
    #             "Location": job["location"],
    #             "Posted": job["posted"],
    #             "Link": job["link"],
    #         }

    #         dfff2 = pd.DataFrame(
    #             create_dict, index=[0])
    #         df_stepstone = df_stepstone.append(dfff2, ignore_index=True)


    # else:
    #     st.write("No results found.")

    # if jobs_kimeta:
    #     df_kimeta = pd.DataFrame()
    #     for job in jobs_kimeta:

    #         create_dict = {
    #             "Title": job["title"],
    #             "Company": job["company"],
    #             "Location": job["location"],
    #             "Posted": job["posted"],
    #             "Link": job["link"],
    #         }

    #         dffff2 = pd.DataFrame(
    #             create_dict, index=[0])
    #         df_kimeta = df_kimeta.append(dffff2, ignore_index=True)

    # if jobs_jobware:
    #     df_jobware = pd.DataFrame()
    #     for job in jobs_jobware:

    #         create_dict = {
    #             "Title": job["Title"],
    #             "Company": job["Company"],
    #             "Location": job["Location"],
    #             "Posted": job["Date"],
    #             "Link": job["Link"],
    #         }

    #         dfffff2 = pd.DataFrame(
    #             create_dict, index=[0])
    #         df_jobware = df_jobware.append(dfffff2, ignore_index=True)



        df = pd.DataFrame()
        df = df.append(jobs_ebay, ignore_index=True)
        df = df.append(jobs_indeed, ignore_index=True)
        df = df.append(jobs_stepstone, ignore_index=True)
        df = df.append(jobs_kimeta, ignore_index=True)
        df = df.append(jobs_jobware, ignore_index=True)
        st.write(df)

    # ddfff = df.append(dff, ignore_index=True)
    # dddfff = ddfff.append(dfff, ignore_index=True)
    # st.write(dddfff)

        csv = convert_df(df)

        st.download_button(
            label="Download",
            data=csv,
            file_name='df.csv',
            mime='text/csv',
        )


# if st.button('Run'):
#         pass



        
        # df = pd.DataFrame(jobs)


    # df = scrape_jobs(title1, location1)
    # df = pd.DataFrame(df)
    # print(df)



    # st.write('hello there')
# else:
#     st.write(' ')




# progress_bar = st.progress(0)
# status_text = st.empty()
# last_rows = np.random.randn(1, 1)
# # chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
# #     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
# st.button("Re-run")
# st.button('Download CSV', dfff.to_csv('data.csv'))


if __name__ == "__main__":
    main()