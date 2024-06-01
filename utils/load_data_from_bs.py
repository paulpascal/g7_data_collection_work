import os
import time
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

from config import CACHE_TTL, AppTabs

load_dotenv()

SCRAPE_URLS = {
    AppTabs.FRIDGES_FREEZERS:  "https://www.expat-dakar.com/refrigerateurs-congelateurs",
    AppTabs.AIR_CONDITIONERS: "https://www.expat-dakar.com/climatisation",
    AppTabs.COOKERS_OVENS:     "https://www.expat-dakar.com/cuisinieres-fours",
    AppTabs.WASHING_MACHINES: "https://www.expat-dakar.com/machines-a-laver"
}


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def scrape_and_clean_data(tab, nb_of_pages):
  df = pd.DataFrame()
  url = SCRAPE_URLS[tab]
  if url:
    for page in range(1, nb_of_pages + 1):
      data = []
      url   = f'{url}?page={page}'
      resp  = _get_page_bypass_cf(url)
      bsoup = bs(resp.text, 'html.parser')
      containers = bsoup.find_all('div', class_ ='listings-cards__list-item')

      for container in containers:
        try:
          item_link  = container.find('a', class_ ='listing-card__inner')['href']
          item_page_content  = _get_page_bypass_cf(item_link)
          item_bsoup = bs(item_page_content.text, 'html.parser')

          details_page_container = item_bsoup.find('div', class_ ='listing-item__info')
          details = details_page_container.find('h1', class_='listing-item__header').text.strip()
          condition = details_page_container.find('dd', class_='listing-item__properties__description').text.strip()
          price = int(
            details_page_container.find('span', class_ ='listing-card__price__value 1').text
            .strip()
            .replace('\u202f', '')
            .replace(' F Cfa', '')
          )
          address = details_page_container.find('span', class_='listing-item__address-location').text.strip()
          region = details_page_container.find('span', class_='listing-item__address-region').text.strip()
          full_address = f'{address} {region}'
          images = item_bsoup.find('div', class_='gallery__image__inner')
          image_link = images.find('img')['src']

          data.append({
            'details': details,
            'etat':    condition,
            'adresse': full_address,
            'prix': price,
            'image_lien': image_link,
          })
        except:
          pass

      current_page_df = pd.DataFrame(data)
      df = pd.concat([df, current_page_df], axis = 0).reset_index(drop = True)
  else:
    _error_message('Could not display data for this tab')
  return df


def _error_message(message):
  alert = st.error(message)
  time.sleep(3)
  alert.empty()


def _get_page_bypass_cf(url):
  apikey = os.getenv('CF_BYPASSER_API_KEY')
  apiHost = os.getenv('CF_BYPASSER_API_HOST')
  params = {
    'url': url,
    'apikey': apikey,
    'js_render': 'true',
  }
  response = requests.get(apiHost, params=params)
  return response
