import streamlit as st
import requests

# URL of your backend API
API_URL = "http://127.0.0.1:8000/api/news/"  # adjust if running on another host/port

st.set_page_config(page_title="News Summarizer", layout="wide")

st.title("📰 AI-Powered News Summarizer")

# Input box
topic = st.text_input("Enter a news topic:", placeholder="e.g., India-America relations, AI in healthcare...")

if st.button("Get Summary"):
    if not topic.strip():
        st.warning("⚠️ Please enter a valid topic.")
    else:
        with st.spinner("Fetching and summarizing news..."):
            try:
                response = requests.post(API_URL, json={"topic": topic}, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Show Summary
                    st.subheader("📝 Summary")
                    st.write(data.get("summary", "No summary available."))

                    # Show Top 5 Articlesf
                    articles = data.get("articles", [])[:5]
                    if articles:
                        st.subheader("🔗 Top Articles")

                        for idx, article in enumerate(articles, start=1):
                            with st.container():
                                st.markdown("---")  # divider between cards
                                col1, col2 = st.columns([4, 1])  # wider left, narrow right

                                with col1:
                                    st.markdown(
                                        f"### {idx}. [{article['title']}]({article['url']})"
                                    )
                                    st.markdown(
                                        # f"**Source:** {article.get('source','Unknown')}  \n"
                                        f"**Description:** {article.get('description','No description available.')}"
                                    )

                                with col2:
                                    # optional: show an image if you include 'urlToImage' in articles
                                    if article.get("urlToImage"):
                                        st.image(article["urlToImage"], use_column_width=True)
                    else:
                        st.info("No articles found.")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
