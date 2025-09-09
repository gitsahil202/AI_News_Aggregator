import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from openai import OpenAI
from dotenv import load_dotenv
import requests
from newspaper import Article
# Create your views here.

load_dotenv()

def fetch_articles(topic):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 4,
        "apiKey": os.getenv("NEWS_API_KEY"),
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException:
        return []

    articles = []
    for item in data.get("articles", []):
        articles.append(
            {
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
                "full_text":None
            }
        )
    return articles


def add_text(articles, max_chars=2000):
    for item in articles:
        url = item.get("url")
        full_text = None
        if url:
            try:
                article = Article(url)
                article.download()
                article.parse()
                text = article.text.strip()
                if text:
                    full_text = text[:max_chars]
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                full_text = None
        else:
            print("Skipping article without URL")
        item["full_text"] = full_text

    return articles

def combine_text(articles):
    max_chars=12000
    combined_texts=[]

    for idx, item in enumerate(articles, start=1):
        full_text=item.get("full_text")
        if full_text:
            combined_texts.append(f"{idx}. {full_text.strip()}")

    combined_text = "\n\n".join(combined_texts)

    if len(combined_text) > max_chars:
        combined_text = combined_text[:max_chars]
    
    if combined_text:
        return combined_text
    else:
        return "Couldn't find news"



def validate_topic(topic):
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt=(
        '''You are an expert News validator who specialises in checking whether a certain topic can be a topic of news or not. When prompted with a text consider that entire text as a topic and draw a valid conclusion whether the given topic can be a topic of news or not. Make your judgement based on if we that topic is searched on the internet then relevant news article of recent time will come up or not. Strictly reply with either 'yes' or 'no' in lowercase letters. Yes if you find the topic relevant and worthy of news and no if you dont think so.
        '''
    )
    try:
        response=client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role":"system","content":prompt},
                {"role":"user","content":topic}
            ],
        )
        print(response.output_text)
        return response.output_text
    except Exception as e:
        return Response({"error":str(e)})

def NewsSummary(text):
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    prompt=(
        '''You are a news summarizer. You will be given text from multiple top news articles on a single topic.
        Instructions:
        1. If most articles describe the same news event, create ONE unified summary in a concise, neutral tone.
        2. If the articles present different views or perspectives, summarize the key points from each and mention that multiple perspectives exist.
        3. Keep the summary clear, professional, and fact-based.
        4. Avoid redundancy and do not copy text directly from the articles.
        5.  Avoid repetition and do not list every article individually.
#         '''
    )
    try:
        response=client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role":"system","content":prompt},
                {"role":"user","content":text}
            ],
        )
        print(response.output_text)
        return response.output_text
    except Exception as e:
        return Response({"error":str(e)})




class SummaryView(APIView):
    def post(self,request):
        topic=request.data.get('topic',None)

        if not topic:
            return Response({'error':'Please enter a valid news topic'},status=400)

        validity=validate_topic(topic)
        if(validity=="no"):
            return Response({'error':'Please enter a relevant topic of news'},status=400) 

        articles=fetch_articles(topic)
        text_articles=add_text(articles)
        combined_text=combine_text(text_articles)
        final=NewsSummary(combined_text)
        return Response({"summary":final},status=200)
