

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
import json

def fetch_asset_urls(response):
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all image tags (img) on the page
    main = soup.find_all('main')
    img_tags = main[0].find_all('img')
    bg_image = main[0].find_all(class_='bose-story-block__backgroundContainer') + main[0].find_all(class_='bose-pageHeader__backgroundContainer')
    poster = main[0].find_all('video')
    img_tags = bg_image + img_tags + poster
    bg_image += main[0].find_all(class_='bose-ecommerceArea')[0].find_all('img') if main[0].find_all(class_='bose-ecommerceArea') else []
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
            if '1280w' in img['data-bgset'] and '1920w' in img['data-bgset']:
                image_urls.append(img['data-bgset'].split('1280w, ')[1].split('1920w')[0].replace("//assets","https://assets"))
            elif '160w' in img['data-bgset']:
                image_urls.append(img['data-bgset'].split('160w')[0].replace("//assets","https://assets"))
            else:
                image_urls.append(img['data-bgset'].split('320w')[0].split('1280w')[0].replace("//assets","https://assets"))
        elif 'data-srcset' in img.attrs:
            if '1280w' in img['data-srcset'] and '1920w' in img['data-srcset']:
                image_urls.append(img['data-srcset'].split('1280w, ')[1].split('1920w')[0].replace("//assets","https://assets"))
            elif '160w' in img['data-srcset']:
                image_urls.append(img['data-srcset'].split('160w')[0].replace("//assets","https://assets"))
            else:
                image_urls.append(img['data-srcset'].split('320w')[0].split('1280w')[0].replace("//assets","https://assets"))
        elif 'data-src' in img.attrs:
            if '160w' in img['data-src']:
                image_urls.append(img['data-src'].split('160w')[0].replace("//assets","https://assets"))
            else:
                image_urls.append(img['data-src'].split('320w')[0].split('1280w')[0].replace("//assets","https://assets"))
        elif 'src' in img.attrs:
            if "assets.bose.com" in img['src']:
                if '160w' in img['src']:
                    image_urls.append(img['src'].split('160w')[0].replace("//assets","https://assets"))
                else:
                    image_urls.append(img['src'].split('320w')[0].split('1280w')[0].replace("//assets","https://assets"))
            else:
                other_urls.append(img['src'].replace("//static","https://static"))
                other = True
        elif 'poster' in img.attrs:
            if "assets.bose.com" in img['poster']:
                if '160w' in img['poster']:
                    image_urls.append(img['poster'].split('160w')[0].replace("//assets","https://assets"))
                else:
                    image_urls.append(img['poster'].split('320w')[0].split('1280w')[0].replace("//assets","https://assets"))
            else:
                other_urls.append(img['poster'].replace("//static","https://static"))
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
        elif img in poster:
            if other:
                other_image_position.append('Video poster')
            else:
                image_position.append('Video poster')
        else:
            if other:
                other_image_position.append('Body image')
            else:
                image_position.append('Body image')
            
    # Find all elements with the specified class
    # elements = soup.find_all(class_="productDocuments")
    download_button = soup.find_all('div', class_="buttonLink")
    zip_download = soup.find_all('a', class_="bose-richText__link")
    elements = soup.find_all('div', attrs={'lpos': "Downloads region area"}) + \
        soup.find_all('div', attrs={'lpos': "Download region area"}) + download_button + zip_download
    elements = soup.find_all('div', class_='bose-cta--show') + elements + soup.find_all('div', class_='linkButtonAttachment') +\
        soup.find_all('div', class_='-download')
    tech_elements = soup.find_all(class_="productList") + soup.find_all(class_="productReference")

    # Extract href attributes
    assets = []
    other_assets = []
    asset_label = []
    other_asset_label = []
    asset_text = []
    other_asset_text = []
    for element in elements:
        a_tags = element.find_all('a')
        try:
            if element in download_button and 'download' not in str(a_tags[1].text).lower():
                continue
        except:
            pass
        try:
            if element in zip_download:
                a_tags = [element]
                if 'download' not in str(a_tags[0].text).lower():
                    continue
        except:
            pass
        for asset in a_tags:
            if asset.get('href'):
                if "assets.bose.com" in asset.get('href'):
                    assets.append(asset.get('href').replace("//assets","https://assets"))
                    label = asset.find_previous(class_='bose-list__title')
                    asset_label.append(label.text if label and element not in tech_elements else None)
                    asset_text.append(asset.text)
                else:
                    other_assets.append(asset.get('href').replace("/en_us","https://www.boseprofessional.com/en_us") \
                        if str(asset.get('href'))[0]=='/' else asset.get('href'))
                    label = asset.find_previous(class_='bose-list__title')
                    other_asset_label.append(label.text if label and element not in tech_elements else None)
                    other_asset_text.append(asset.text)

    elements = soup.find_all(class_="productList")
    elements += soup.find_all(class_="productReference") + soup.find_all(class_='productCatalogList')

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
        
    catlog = main[0].find_all(class_='search-organism-container')
    if catlog and main[0].find_all(class_='productCatalogList'):
        catlog_json = json.loads(catlog[0]['data-search-data'])
        products = catlog_json.get('products')
        if products:
            for prod in products:
                if prod.get('mainImage'):
                    if len(prod.get('variants', []))==2 and len(prod.get('colors', []))==2:
                        image_urls.append(prod['variants'][1]['images']['smallImageURL'] \
                            if prod.get('variants')[1]['color']['code']=='black' else prod['variants'][0]['images']['smallImageURL'])
                    else:
                        image_urls.append(prod['mainImage'])
                    image_position.append('Catlog image')
                if prod.get('proCTAUrl'):
                    assets.append(prod['proCTAUrl'])
                    asset_text.append('TECHNICAL INFO')
                if prod.get('url'):
                    related_pages.append(prod['url'])
                    related_labels.append(prod['name'])
                
            

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