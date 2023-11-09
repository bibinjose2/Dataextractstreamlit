

"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_asset_urls(response):
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags (img) on the page
    main = soup.find_all('main')
    img_tags = main[0].find_all('img')
    bg_image = main[0].find_all(class_='bose-story-block__backgroundContainer') + main[0].find_all(class_='bose-pageHeader__backgroundContainer')
    img_tags = bg_image + img_tags
    bg_image += main[0].find_all(class_='bose-ecommerceArea')[0].find_all('img')
    related_page_images = []
    related_page_images += soup.find_all(class_="productList")[0].find_all('img') if soup.find_all(class_="productList") else [] 
    related_page_images += soup.find_all(class_="productReference")[0].find_all('img') if soup.find_all(class_="productReference") else []

    # Extract image URLs
    image_urls = []
    image_position = []
    other_urls =[]
    other_image_position = []
    related_pages = []
    for img in img_tags:
        other = False
        if 'data-bgset' in img.attrs:
            if '160w' in img['data-bgset']:
                image_urls.append(img['data-bgset'].split('160w')[0].replace("//assets","https://assets"))
            else:
                image_urls.append(img['data-bgset'].split('320w')[0].replace("//assets","https://assets"))
        elif 'data-srcset' in img.attrs:
            image_urls.append(img['data-srcset'].split('320w')[0].replace("//assets","https://assets"))
        elif 'src' in img.attrs:
            if "assets.bose.com" in img['src']:
                if '160w' in img['data-bgset']:
                    image_urls.append(img['src'].split('160w')[0].replace("//assets","https://assets"))
                else:
                    image_urls.append(img['src'].split('320w')[0].replace("//assets","https://assets"))
            else:
                other_urls.append(img['src'].replace("//static","https://static"))
                other = True
        else:
            continue

        if img in bg_image:
            if other:
                other_image_position.append('Cover image')
            else:
                image_position.append('Cover image')
        elif img in related_page_images:
            if other:
                other_image_position.append('Related page image')
            else:
                image_position.append('Related page image')
        else:
            if other:
                other_image_position.append('Body image')
            else:
                image_position.append('Body image')

    # Find all elements with the specified class
    # elements = soup.find_all(class_="productDocuments")
    elements = soup.find_all('div', attrs={'lpos': "Downloads region area"})
    elements = soup.find_all('div', class_='proCallToAction') + elements

    # Extract href attributes
    assets = []
    other_assets = []
    asset_label = []
    other_asset_label = []
    asset_text = []
    other_asset_text = []
    for element in elements:
        a_tags = element.find_all('a')
        for asset in a_tags:
            if asset.get('href'):
                if "assets.bose.com" in asset.get('href'):
                    assets.append(asset.get('href').replace("//assets","https://assets"))
                    label = asset.find_previous(class_='bose-list__title')
                    asset_label.append(label.text if label else None)
                    asset_text.append(asset.text)
                else:
                    other_assets.append(asset.get('href'))
                    label = asset.find_previous(class_='bose-list__title')
                    other_asset_label.append(label.text if label else None)
                    other_asset_text.append(asset.text)

    elements = soup.find_all(class_="productList")
    elements += soup.find_all(class_="productReference")

    # Extract href attributes
    related_labels_pages = {}
    for element in elements:
        # print(element)
        a_tags = element.find_all('a')
        for asset in a_tags:
            if asset.get('href') and "//assets" not in asset.get('href'):
                related_labels_pages["https://www.boseprofessional.com"+asset.get('href')] = asset.text

    related_pages = []
    related_labels = []
    for label in related_labels_pages:
        related_labels.append(related_labels_pages[label])
        related_pages.append(label)

    return  image_urls, assets, other_urls, other_assets, related_pages,\
        related_labels, asset_label, other_asset_label,asset_text, other_asset_text,\
            image_position, other_image_position

def scrape_data(page_url):
    response = requests.get(page_url)

    # Check if the request was successful
    if response.status_code == 200:
        img_urls, asset_urls, other_urls, other_assets, related_pages, related_labels,\
            asset_label, other_asset_label, asset_text, other_asset_text ,\
                image_position, other_image_position= fetch_asset_urls(response)

        df_bose_images = pd.DataFrame({'Bynder Image URLs': img_urls})
        df_image_position = pd.DataFrame({'Bynder Image Position': image_position})
        df_assets = pd.DataFrame({'Bynder Asset URLS': asset_urls})
        df_assets_text = pd.DataFrame({'Bynder Asset Text': asset_text})
        df_assets_label = pd.DataFrame({'Bynder Asset Title': asset_label})
        df_other_images = pd.DataFrame({'Other image URLS': other_urls})
        df_other_image_position = pd.DataFrame({'Other Image Position': other_image_position})
        df_other_assets = pd.DataFrame({'Other asset URLS': other_assets})
        df_other_assets_text = pd.DataFrame({'Other Asset Text': other_asset_text})
        df_other_assets_label = pd.DataFrame({'Other Asset Title': other_asset_label})
        df_related_pages = pd.DataFrame({'Related pages': related_pages})
        related_labels = pd.DataFrame({'Related labels': related_labels})

        df_combined = pd.concat([df_bose_images, df_image_position, df_assets, df_assets_text, df_assets_label, \
            df_other_images, df_other_image_position, df_other_assets, df_other_assets_text, df_other_assets_label, \
                df_related_pages, related_labels], axis=1)

        return df_combined

    else:
        return response.status_code


bose_url = st.text_input("Input Bose Professional URL", None)
uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file:
   df_page_urls = pd.read_csv(uploaded_file)
   output_data = []

   for index, row in df_page_urls.iterrows(): 
        df_combined = scrape_data(row['URL'].strip())
        # output_data.append({'URL': row['URL'], 'ScrapedData': df_combined})
        st.header(row['URL'])
        df_combined


if bose_url:

    df_combined =scrape_data(bose_url.strip())

    df_combined