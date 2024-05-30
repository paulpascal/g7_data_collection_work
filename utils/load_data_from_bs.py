import time
import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

from config import CACHE_TTL, AppTabs

SCRAPE_URLS = {
    AppTabs.FRIDGE_FREEZER:  "https://www.expat-dakar.com/refrigerateurs-congelateurs",
    AppTabs.AIR_CONDITIONER: "https://www.expat-dakar.com/climatisation",
    AppTabs.COOKER_OVEN:     "https://www.expat-dakar.com/cuisinieres-fours",
    AppTabs.WASHING_MACHINE: "https://www.expat-dakar.com/machines-a-laver"
}


@st.cache_data(ttl=CACHE_TTL, show_spinner="Fetching data...")
def scrape_and_clean_data(tab, nb_of_pages):
  if tab == AppTabs.FRIDGE_FREEZER:
    return load_fride_freezer_data(tab, SCRAPE_URLS[tab], nb_of_pages)
  elif tab == AppTabs.AIR_CONDITIONER:
    return load_air_conditionner_data(tab, SCRAPE_URLS[tab], nb_of_pages)
  elif tab == AppTabs.COOKER_OVEN:
    return load_cooker_oven_data(tab, SCRAPE_URLS[tab], nb_of_pages)
  elif tab == AppTabs.WASHING_MACHINE:
    return load_washing_machines_data(tab, SCRAPE_URLS[tab], nb_of_pages)
  else:
    _error_message('Could not display data for this tab')


# Load Fridges and freezers Data with BeautifulSoup
def load_fride_freezer_data(tab, url, nb_of_page=1):
  data = []

  try:
    # do scrapping
    return pd.DataFrame(data)
  except:
    _error_message(f"Some error occured when fetching data for {tab.value}!")
    return pd.DataFrame(data)


# Load Air Conditionners Data with BeautifulSoup
def load_air_conditionner_data(tab, url, nb_of_page=1):
  data = []

  try:
    # do scrapping
    return pd.DataFrame(data)
  except:
    _error_message(f"Some error occured when fetching data for {tab.value}!")
    return pd.DataFrame(data)


# Load cookesr and ovens Data with BeautifulSoup
def load_cooker_oven_data(tab, url, nb_of_page=1):
  data = []

  try:
    # do scrapping
    return pd.DataFrame(data)
  except:
    _error_message(f"Some error occured when fetching data for {tab.value}!")
    return pd.DataFrame(data)


# Load washing machines Data with BeautifulSoup
def load_washing_machines_data(tab, url, nb_of_page=1):
  data = []

  try:
    # do scrapping
    return pd.DataFrame(data)
  except:
    _error_message(f"Some error occured when fetching data for {tab.value}!")
    return pd.DataFrame(data)


def _error_message(message):
  alert = st.error(message)
  time.sleep(3)
  alert.empty()
