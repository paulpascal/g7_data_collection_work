import seaborn as sb
import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

from config import AppPages, AppTabs
from utils.load_data_from_bs import scrape_and_clean_data
from utils.load_data_from_ws import load_raw_scraped_data, load_cleaned_scraped_data


def display_scrape_data(nb_of_pages):
    st.markdown('###')
    st.info("Scrape data across multiple pages", icon="🚀")

    for tab in AppTabs:
        with st.expander(tab.value):
            if st.button('Scrape now', key=tab):
                with st.spinner('Scraping data...'):
                    df = scrape_and_clean_data(tab, nb_of_pages)

                st.write('Data dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
                st.dataframe(df, use_container_width=True)


def display_scraped_data():
    st.markdown('###')
    st.info("Display already scraped data (not cleaned)", icon="🗄")
    for tab in AppTabs:
        with st.expander(tab.value):
            df = load_raw_scraped_data(tab)

            st.write('Data dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
            st.dataframe(df, use_container_width=True)


def display_dashboard():
    st.markdown('###')
    st.info("Displaying Dashboard", icon="📊")
    tab_names = [tab.value for tab in AppTabs]
    tabs = st.tabs(tab_names)

    for tab_name, tab in zip(tab_names, AppTabs):
        with tabs[tab_names.index(tab_name)]:
            df = load_cleaned_scraped_data(tab)
            equipment = tab.value

            if not df.empty:
                # Price variation with equipment status (etat) using strip plot
                fig, ax = plt.subplots(figsize=(15, 10))
                sb.stripplot(
                    x='etat', y='prix', hue='etat',
                    data=df, ax=ax, palette="Set2",
                    jitter=True, dodge=True, alpha=0.7, legend=False
                )
                ax.set_title(f'Price variation with {equipment} status')
                st.pyplot(fig)

                # Bar plot for average price by equipment status
                fig, ax = plt.subplots(figsize=(15, 10))
                avg_price = df.groupby('etat')['prix'].mean().reset_index()
                sb.barplot(
                    x='etat', y='prix',
                    hue='prix', data=avg_price,
                    ax=ax, palette="Set3", legend=False
                )
                ax.set_title(f'Average price by {equipment} Status')
                st.pyplot(fig)

                # Top addresses where new cars are found (adresse and etat='Neuf')
                new_cars = df[df['etat'].str.lower() == 'neuf']
                top_new_places = new_cars['adresse'].value_counts().head(5).reset_index()
                top_new_places.columns = ['adresse', 'count']
                fig, ax = plt.subplots(figsize=(15, 10))
                sb.barplot(
                    x='count', y='adresse', ax=ax,
                    hue='adresse', data=top_new_places,
                    palette=sb.color_palette("coolwarm", len(top_new_places)), legend=False
                )
                ax.set_title(f'Top places where new {equipment} are found')
                st.pyplot(fig)
            else:
                st.caption("😔 No data available currently for this tab.")


def display_form():
    RATING_FORM_URL = 'https://ee.kobotoolbox.org/single/5e1e80143ad4fc67e50331d68e839312'

    st.markdown('###')
    st.info("Fill Out Application Evaluation Form", icon="📋")
    components.html(
        f"""
        <iframe src="{RATING_FORM_URL}" width="800" height="1100"></iframe>
        """,
        width=800,
        height=1100,

    )


def main():
    title       = 'G7 DATA SCRAPER APP'
    nb_of_pages = 1

    st.set_page_config(
        page_title='G7 DATA SCRAPER APP',
        page_icon=":chart_with_upwards_trend:",
        # layout="wide"
    )
    st.title(f':chart_with_upwards_trend: :orange[{title}]')

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
