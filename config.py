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
  FRIDGES_FREEZERS  = 'Fridges & Freezers'
  AIR_CONDITIONERS  = 'Air Conditioners'
  COOKERS_OVENS     = 'Cookers & Ovens'
  WASHING_MACHINES  = 'Washing Machines'
