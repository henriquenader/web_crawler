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
from selenium.common.exceptions import NoSuchElementException
from ebay import get_ebay
from indeed import get_indeed
# from get_linkedin import get_linkedin
from kimeta import get_kimeta
from stepstone import get_stepstone
from jobware import get_jobware


st.set_page_config(page_title="Job Crawler", page_icon="📈")

st.markdown("# Job Crawler")
# st.sidebar.header("Job Crawler")
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






# ***************************
# def get_kimeta_description(df_link_kimeta):

# link_list = []
# for link in df_link_kimeta:
#     link_list.append(link)

# html_list = []
# for i in link_list:
#     options = Options()
#     options.headless = True
#     driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#     driver.get(i)
#     time.sleep(2)
#     html = driver.page_source
#     html_list.append(html)

# pd.Series(html_list).to_csv('kimeta_html_list.csv')
# htmls = pd.read_csv('kimeta_html_list.csv', index_col=0)['0']
# descriptions = []
# for html in htmls:
#     soup = BeautifulSoup(html, "html.parser")
#     descriptions.append(soup.get_text())

# df_kimeta_description2 = pd.DataFrame({'description': descriptions})

# ********************




def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def main():

    if st.button('Run'):
        try:
            jobs_ebay = get_ebay()
        except:
            st.error('No jobs found on eBay')
            jobs_ebay = pd.DataFrame()

        try:
            jobs_indeed = get_indeed(title1, location1)
        except:
            st.error('No jobs found on Indeed')
            jobs_indeed = pd.DataFrame()

        try:
            jobs_stepstone = get_stepstone(title1, location1, color)
        except:
            st.error('No jobs found on Stepstone')
            jobs_stepstone = pd.DataFrame()
        
        try:
            jobs_kimeta = get_kimeta(title1, location1, color)
        except:
            st.error('No jobs found on Kimeta')
            jobs_kimeta = pd.DataFrame()
        
        try:
            jobs_jobware = get_jobware(title1, location1, color)
        except:
            st.error('No jobs found on Jobware')
            jobs_jobware = pd.DataFrame()


        def get_link_jobware(jobs_jobware):

            if jobs_jobware.empty:
                return pd.DataFrame()
            
            link_list = []
            for link in jobs_jobware['Link']:
                link_list.append(link)

            options = Options()
            options.headless = False
            driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=options)

            html_list = []

            for i in link_list:
                driver.get(i)
                time.sleep(2)
                html = driver.page_source
                html_list.append(html)

            # pd.Series(html_list).to_csv('rodrigo_html_list.csv')
            htmls = pd.Series(html_list)
            # htmls = pd.read_csv('rodrigo_html_list.csv', index_col=0)['0']

            html_script_tags_list = []
            for html in htmls:
                try:
                    soup = BeautifulSoup(html, "html.parser")
                    script_tags = soup.find_all(
                        'script', type='application/ld+json')
                    html_script_tags_list.append(script_tags[1].get_text())
                except:
                    html_script_tags_list.append('')

            dicts = []

            for script in html_script_tags_list:
                dicts.append(json.loads(script))

            df = pd.DataFrame(dicts)

            return df

        try:
            df_jobware_description2 = get_link_jobware(jobs_jobware)
            df_jobware_description2['contact'] = df_jobware_description2['description']
            df_jobware_description2 = df_jobware_description2['contact']
        except:
            st.error('No jobs found on Jobware')
            df_jobware_description2 = pd.DataFrame()

        # ---------------------------

        def get_link_stepstone(jobs_stepstone):
            if jobs_stepstone.empty:
                return pd.DataFrame()
            link_list = []
            for link in jobs_stepstone['Link']:
                link_list.append(link)

            options = Options()
            options.headless = True
            driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=options)

            html_list = []

            for i in link_list:
                driver.get(i)
                time.sleep(2)
                html = driver.page_source
                html_list.append(html)

            htmls = pd.Series(html_list)

            content_list = []
            import json
            for html in htmls:
                try:
                    soup = BeautifulSoup(html, 'html.parser')
                    script = soup.find(
                        'script', id="js-section-preloaded-ContentBlock")
                    script = script.text
                    script = script.split('.ContentBlock = ')[1]
                    script = script.split(';\n')[0]
                    dic = json.loads(script)
                    content = dic['textSectionsData'][4]['content']
                    content_list.append(content)
                except:
                    content_list.append('')

            s = pd.DataFrame({'contact': content_list})

            return s

        try:
            df_stepstone_description2 = get_link_stepstone(jobs_stepstone)
        except:
            st.error('No jobs found on Stepstone')
            df_stepstone_description2 = pd.DataFrame()

        # ---------------------------

        def get_link_kimeta(jobs_kimeta):
            if jobs_kimeta.empty:
                return pd.DataFrame()
            link_list = []
            for link in jobs_kimeta['Link']:
                link_list.append(link)

            options = Options()
            options.headless = True
            driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=options)
            html_list = []

            for i in link_list:
                driver.get(i)
                time.sleep(2)
                html = driver.page_source
                html_list.append(html)

            htmls = pd.Series(html_list)

            descriptions = []
            for html in htmls:
                soup = BeautifulSoup(html, "html.parser")
                descriptions.append(soup.get_text())

            df_kimeta_description2 = pd.DataFrame(
                {'contact': descriptions})

            return df_kimeta_description2

        try:
            df_kimeta_description2 = get_link_kimeta(jobs_kimeta)
        except:
            st.error('No jobs found on Kimeta')
            df_kimeta_description2 = pd.DataFrame()

        # ---------------------------

        jobs_kimeta = jobs_kimeta.reset_index(drop=True)
        jobs_stepstone = jobs_stepstone.reset_index(drop=True)
        jobs_jobware = jobs_jobware.reset_index(drop=True)

        df_kimeta_description2 = df_kimeta_description2.reset_index(drop=True)
        df_stepstone_description2 = df_stepstone_description2.reset_index(
            drop=True)
        df_jobware_description2 = df_jobware_description2.reset_index(
            drop=True)

        jobs_kimeta = pd.concat([jobs_kimeta, df_kimeta_description2], axis=1)
        jobs_stepstone = pd.concat(
            [jobs_stepstone, df_stepstone_description2], axis=1)
        jobs_jobware = pd.concat(
            [jobs_jobware, df_jobware_description2], axis=1)

        df = pd.DataFrame()
        df = df.append(jobs_ebay, ignore_index=True)
        df = df.append(jobs_indeed, ignore_index=True)
        df = df.append(jobs_stepstone, ignore_index=True)
        df = df.append(jobs_kimeta, ignore_index=True)
        df = df.append(jobs_jobware, ignore_index=True)


        # --------

        def find_phones(text):
            text = text.replace('\n', ' ')
            text = text.replace('\t', ' ')
            phones = re.findall(r'\d{2,}[\d/ -]{11,17}\d', text)
            phones = [i.strip() for i in phones if sum(1 for char in i if char.isdigit()) > 8]
            phones = [i for i in phones if sum(1 for char in i if char.isdigit()) < 15]
            return list(set(phones))


        def find_emails(text):
            text = text.replace('\n', ' ')
            text = text.replace('\t', ' ')
            emails = re.findall(r'([a-z]+[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-z]+)', text)
            return list(set(emails))


        def process_table(df):
            # df = df.drop('contact', axis=1)
            df.contact.fillna('', inplace=True)
            df['detected_phones'] = df.contact.apply(find_phones)
            df['detected_emails'] = df.contact.apply(find_emails)
            return df

        df = process_table(df)
        st.write(df)

        csv = convert_df(df)

        st.download_button(
            label="Download",
            data=csv,
            file_name='df.csv',
            mime='text/csv',
        )


if __name__ == "__main__":
    main()
