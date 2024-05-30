import pandas as pd


def get_file_path(tab):
    file_path = f"data/{tab.name.lower()}.csv"
    return file_path


def load_scraped_data(tab):
    try:
        return pd.read_csv(get_file_path(tab))
    except:
        return pd.DataFrame()


def clean_scraped_data(tab):
    try:
        data = load_scraped_data(tab)
        return data
    except:
        return pd.DataFrame()
