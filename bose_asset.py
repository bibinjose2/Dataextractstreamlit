

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
    related_pages = []
    for img in img_tags:
        if 'data-srcset' in img.attrs:
            image_urls.append(img['data-srcset'].split('320w')[0].replace("//assets","https://assets"))

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

    elements = soup.find_all(class_="productList")

    # Extract href attributes
    related_pages = []
    for element in elements:
        print(element)
        a_tags = element.find_all('a')
        related_pages += ["https://www.boseprofessional.com"+asset.get('href') for asset in a_tags if asset.get('href') and "//assets" not in asset.get('href')]
        related_pages = list(set(related_pages))
    return  image_urls, assets, other_urls, related_pages

def scrape_data(page_url):
    response = requests.get(page_url)

    # Check if the request was successful
    if response.status_code == 200:
        img_urls, asset_urls, other_urls, related_pages= fetch_asset_urls(response)

    df_bose_images = pd.DataFrame({'asset.bose image URLs': img_urls})
    df_assets = pd.DataFrame({'asset.bose asset URLS': asset_urls})
    df_other_images = pd.DataFrame({'Other image URLS': other_urls})
    df_related_pages = pd.DataFrame({'Related pages': related_pages})

    df_combined = pd.concat([df_bose_images, df_assets, df_other_images, df_related_pages], axis=1)

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

    df_combined =scrape_data(bose_url)

    df_combined






