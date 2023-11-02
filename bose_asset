

"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Replace the URL with the one you want to scrape
url = "https://www.boseprofessional.com/en_us/products/loudspeakers/line_arrays/arenamatch/arenamatch_am10.html#v=arenamatch_am10_60_black"

bose_url = st.text_input("Input Bose Professional URL", None)

if bose_url:

    # Send an HTTP GET request to the URL
    response = requests.get(bose_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image tags (img) on the page
        img_tags = soup.find_all('img')

        # Extract image URLs
        image_urls = []
        for img in img_tags:
            if 'data-srcset' in img.attrs:
                image_urls.append(img['data-srcset'].split('jcr:content')[0])
            elif 'src' in img.attrs:
                image_urls.append(img['src'])

        # Find all elements with the specified class
        elements = soup.find_all(class_="productDocuments")

        # Extract href attributes
        assets = []
        for element in elements:
            a_tags = element.find_all('a')
            assets += [asset.get('href') for asset in a_tags if asset.get('href')]

        # Create separate DataFrames for image_urls and assets
        df_images = pd.DataFrame({'Image URLs': image_urls})
        df_assets = pd.DataFrame({'Asset HREFs': assets})

        # Concatenate DataFrames along the columns (axis=1)
        df_combined = pd.concat([df_images, df_assets], axis=1)

        # Print the first few rows of the combined DataFrame
        df_combined



    else:
        print('Failed to retrieve the webpage.')



    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
