

"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_asset_urls(response):
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags (img) on the page
    img_tags = soup.find_all('img')

    # Extract image URLs
    image_urls = []
    other_urls =[]
    for img in img_tags:
        if 'data-srcset' in img.attrs:
            image_urls.append(img['data-srcset'].split('jcr:content')[0].replace("//assets","https://assets"))
        elif 'src' in img.attrs:
            if "assets.bose.com" in img['src']:

               image_urls.append(img['src'].replace("//assets","https://assets"))
            else:
                other_urls.append(img['src'])


    # Find all elements with the specified class
    elements = soup.find_all(class_="productDocuments")

    # Extract href attributes
    assets = []
    for element in elements:
        a_tags = element.find_all('a')
        assets += [asset.get('href').replace("//assets","https://assets") for asset in a_tags if asset.get('href')]

    return  image_urls, assets, other_urls

def scrape_data(page_url):
    response = requests.get(page_url)

    # Check if the request was successful
    if response.status_code == 200:
        img_urls, asset_urls, other_urls = fetch_asset_urls(response)

    df_bose_images = pd.DataFrame({'Bynder URLs': img_urls})
    df_assets = pd.DataFrame({'Asset URLS': asset_urls})
    df_other_images = pd.DataFrame({'Other image URLS': other_urls})

    df_combined = pd.concat([df_bose_images, df_assets, df_other_images], axis=1)

    return df_combined


bose_url = st.text_input("Input Bose Professional URL", None)
uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file:
   df_page_urls = pd.read_csv(uploaded_file)
   output_data = []

   for index, row in df_page_urls.iterrows():
        df_combined = scrape_data(row['URL'])
        output_data.append({'URL': row['URL'], 'ScrapedData': df_combined})
        st.header(row['URL'])
        df_combined




if bose_url:

    df_combined =scrape_data(page_url)

    df_combined






