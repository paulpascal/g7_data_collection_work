import pandas as pd
import streamlit as st

from config import CACHE_TTL


def get_datasource_path(tab, clean=True):
    data_type = 'cleaned' if clean else 'raw'
    file_path = f"data/{data_type}/{tab.name.lower()}.csv"
    return file_path


@st.cache_data(ttl=CACHE_TTL, show_spinner="Loading data...")
def load_raw_scraped_data(tab):
    try:
        datasource_path = get_datasource_path(tab, False)
        return pd.read_csv(datasource_path)
    except:
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_TTL, show_spinner="Loading data...")
def load_cleaned_scraped_data(tab):
    try:
        datasource_path = get_datasource_path(tab, True)
        return pd.read_csv(datasource_path)
    except:
        return pd.DataFrame()
