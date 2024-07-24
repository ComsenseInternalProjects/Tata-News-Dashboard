import streamlit as st
import sqlite3
import os
import pandas as pd
from PIL import Image
from src.google_news import fetch_news, extract_articles, save_to_database, bulk_runs
from src.extract_article import get_article
from src.relevancy import analyze_sentiment, is_relevant
from src.analyse import fetch_insights


st.set_page_config(
    page_title="Data to Insights",
    layout="wide",
    page_icon=":tata_motors:"
)


image_path = os.path.join(os.path.dirname(__file__), 'data', 'tata_motors.jpg')
image = Image.open(image_path)
st.image(image, width=100)

st.title("Tata Motors Commercial Vehicles News Dashboard")
st.markdown("***")

if st.button("Fetch and Process News"):
    with st.spinner('Fetching and processing news...'):
        # Fetch and process data for commercial vehicles and automobile industry
        news_data = bulk_runs(robotId="77f195c0-294e-48f9-9962-1ceac580a9f7", bulkRunId="f22b2762-da40-4582-b465-dc3ea130aac6")
        articles = extract_articles(news_data)
        save_to_database(articles, "bulk_news")

        st.success("Data fetched and saved to database successfully!")

        conn = sqlite3.connect('src/tata_news.db')
        cursor = conn.cursor()

        # Fetch articles from the database
        cursor.execute("SELECT title, link, DATE(last_updated_date) FROM bulk_news WHERE DATE(last_updated_date) = DATE('now')")
        articles = cursor.fetchall()

        # Extract article titles, links, and publish dates from the tuples
        article_info = [(article[0], article[1], article[2]) for article in articles]

        important_news = []
        latest_news = []

        for title, link, publish_at in article_info:
            body, url = get_article(str(title))
            if body is not None:
                latest_news.append((title, body, url, publish_at))

                if analyze_sentiment(body) or is_relevant(body):
                    important_news.append((title, body, url, publish_at))

        # Display latest news in tabular format
        st.header("Latest News")
        latest_news_df = pd.DataFrame(latest_news, columns=["Title", "Content", "URL", "Publish AT"])
        st.dataframe(latest_news_df)

        # Display important news in tabular format
        st.header("Important News")
        important_news_df = pd.DataFrame(important_news, columns=["Title", "Content", "URL", "Publish AT"])
        st.dataframe(important_news_df)

        # Analyze important news using OpenAI LLM
        st.header("Important News Analysis")
        analysis = []
        for _, row in important_news_df.iterrows():
            title = row['Title']
            url = row['URL']
            content = row['Content']
            publish_at = row['Publish AT']
            insights = fetch_insights(content)
            analysis.append((url, title, insights, publish_at))

        analysis_df = pd.DataFrame(analysis, columns=["URL", "Title", "Analysis", "Publish AT"])
        st.dataframe(analysis_df)

        conn.close()