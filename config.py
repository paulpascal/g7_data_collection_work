from enum import Enum

CACHE_TTL = 24 * 60 * 60


class AppPages(Enum):
  SCRAPE_DATA      = 'Scrape data using BeautifulSoup'
  DOWNLOAD_DATA    = 'Download scraped data'
  DATA_DASHBOARD   = 'Dashboard of data'
  RATE_APP         = 'Rate this app'

  @classmethod
  def get_items(cls):
    return [option.value for option in cls]


class AppTabs(Enum):
  FRIDGE_FREEZER   = 'Réfrigérateurs & Congélateurs'
  AIR_CONDITIONER  = 'Climatisation'
  COOKER_OVEN      = 'Cuisinières & Fours'
  WASHING_MACHINE  = 'Machines à laver'

