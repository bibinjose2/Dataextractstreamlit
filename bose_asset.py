

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
            image_urls.append(img['data-srcset'].split('jcr:content')[0])
        elif 'src' in img.attrs:
            if "assets.bose.com" in img['src']:
               image_urls.append(img['src'])
            else:
                other_urls.append(img['src'])


    # Find all elements with the specified class
    elements = soup.find_all(class_="productDocuments")

    # Extract href attributes
    assets = []
    for element in elements:
        a_tags = element.find_all('a')
        assets += [asset.get('href') for asset in a_tags if asset.get('href')]

    return  image_urls, assets, other_urls

bose_url = st.text_input("Input Bose Professional URL", None)

if bose_url:

    # Send an HTTP GET request to the URL
    response = requests.get(bose_url)

    # Check if the request was successful
    if response.status_code == 200:

        img_urls , asset_urls, other_urls = fetch_asset_urls(response)


        # Create separate DataFrames for image_urls and assets
        df_bose_images = pd.DataFrame({'Bynder URLs': img_urls})
        df_assets = pd.DataFrame({'Asset URLS': asset_urls})
        df_other_images= pd.DataFrame({'Other image URLS': other_urls})

        # Concatenate DataFrames along the columns (axis=1)
        df_combined = pd.concat([df_bose_images, df_assets,df_other_images ], axis=1)

        # Print the first few rows of the combined DataFrame
        df_combined


    else:
        print('Failed to retrieve the webpage.')




