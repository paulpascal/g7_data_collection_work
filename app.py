import streamlit as st
import streamlit.components.v1 as components
from config import CACHE_TTL, AppPages, AppTabs
from utils.load_data_from_bs import scrape_and_clean_data
from utils.load_data_from_ws import clean_scraped_data, load_scraped_data


@st.cache_data(ttl=CACHE_TTL, show_spinner="Fetching data...")
def display_scrape_data(nb_of_pages):
    st.markdown('###')
    st.info("Scrape data across multiple pages", icon="ℹ️")

    scrape_urls = {
        AppTabs.FRIDGE_FREEZER:  "https://www.expat-dakar.com/refrigerateurs-congelateurs",
        AppTabs.AIR_CONDITIONER: "https://www.expat-dakar.com/climatisation",
        AppTabs.COOKER_OVEN:     "https://www.expat-dakar.com/cuisinieres-fours",
        AppTabs.WASHING_MACHINE: "https://www.expat-dakar.com/machines-a-laver"
    }

    for tab in AppTabs:
        with st.expander(tab.value):
            # if st.button(f"Scrape {tab.value}"):
            st.write(f"Scraping {nb_of_pages} pages from {scrape_urls[tab]}")
            with st.spinner("Scraping data..."):
                data = scrape_and_clean_data(tab, nb_of_pages)
            st.dataframe(data)


@st.cache_data(ttl=CACHE_TTL, show_spinner="Fetching data...")
def display_scraped_data():
    st.markdown('###')
    st.info("Display already scraped data (not cleaned)", icon="ℹ️")
    for tab in AppTabs:
        with st.expander(tab.value):
            data = load_scraped_data(tab)
            st.dataframe(data)


@st.cache_data(ttl=CACHE_TTL, show_spinner="Fetching data...")
def display_dashboard():
    st.markdown('###')
    st.info("Displaying Dashboard", icon="ℹ️")
    tab_names = [tab.value for tab in AppTabs]
    tabs = st.tabs(tab_names)

    for tab_name, tab in zip(tab_names, AppTabs):
        with tabs[tab_names.index(tab_name)]:
            clean_scraped_data(tab)
            st.write(f"Dashboard for {tab.value}")


def display_form():
    RATING_FORM_URL = 'https://ee.kobotoolbox.org/i/'

    st.markdown('###')
    st.info("Fill Out Application Evaluation Form", icon="ℹ️")
    components.html(
        f"""
        <iframe src="{RATING_FORM_URL}" width="800" height="1100"></iframe>
        """,
        width=800,
        height=1100,

    )


def main():
    title       = 'G7 Data Scraper App'
    nb_of_pages = 1

    st.set_page_config(
        page_title=title,
        page_icon=":chart_with_upwards_trend:"
    )
    st.title(title)

    with st.sidebar:
        st.header("Configuration")

        app_pages = AppPages.get_items()
        selected_page = st.selectbox(
            label="Choose an option from this menu",
            options=app_pages,
        )
        nb_of_pages = st.number_input(
            label="Number of page to scrape",
            value=1,
            disabled= selected_page != AppPages.SCRAPE_DATA.value
        )

        st.markdown("---")
        st.caption(
            '''This app allows you to download scraped data on various equipements from Expat-Dakar.'''
        )
        st.caption(
            '''**Python libraries:** bs4, numpy, pandas, seaborn, streamlit'''
        )
        st.caption(
            '''**Data source:** [Expat-Dakar](https://www.expat-dakar.com/)'''
        )
        st.markdown(
        '''
        <br/>
        <h6>Made in &nbsp
          <img
            src="https://streamlit.io/images/brand/streamlit-mark-color.png"
            alt="Streamlit logo" height="16">&nbsp by:
        </h6>
        <ul>
          <li><a href="https://github.com/paulpascal">@paulpascal</a></li>
          <li><a href="https://github.com/gbadabizo">@gbadabizo</a></li>
          <li><a href="https://github.com/abdelaziz2016">@Abdelaziz</a></li>
          <li><a href="mailto:moulopautboussenguithibauld@gmail.com
">@thibauld</a></li>
        </ul>
        ''',
        unsafe_allow_html=True,
    )

    if selected_page == AppPages.SCRAPE_DATA.value:
        display_scrape_data(nb_of_pages)
    elif selected_page == AppPages.DOWNLOAD_DATA.value:
        display_scraped_data()
    elif selected_page == AppPages.DATA_DASHBOARD.value:
        display_dashboard()
    elif selected_page == AppPages.RATE_APP.value:
        display_form()


if __name__ == "__main__":
  main()
