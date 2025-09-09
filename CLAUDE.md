# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is an AI-powered news aggregator with two main components:

### Backend (Django + DRF)
- **Location**: `./news_agg/`
- **Framework**: Django 5.2.6 with Django REST Framework
- **Main app**: `news` app containing the core functionality
- **Key files**:
  - `news_agg/settings.py` - Django settings
  - `news/views.py:135` - `SummaryView` API endpoint for news summarization
  - `news/views.py:13` - `fetch_articles()` fetches from NewsAPI
  - `news/views.py:43` - `add_text()` scrapes full article content using newspaper3k
  - `news/views.py:85` - `validate_topic()` validates topics using OpenAI
  - `news/views.py:105` - `NewsSummary()` generates summaries using OpenAI

### Frontend (Streamlit)
- **Location**: `./news_frontend/page.py`
- **Framework**: Streamlit web app
- **Purpose**: User interface for entering topics and displaying summaries
- **API Integration**: Makes POST requests to Django backend at `http://127.0.0.1:8000/api/news/`

## Common Development Commands

### Backend (Django)
```bash
# Navigate to Django project
cd news_agg

# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Frontend (Streamlit)
```bash
# Run Streamlit app
streamlit run news_frontend/page.py
```

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Environment variables required in .env:
# OPENAI_API_KEY - OpenAI API key for summarization
# NEWS_API_KEY - NewsAPI.org key for fetching articles
```

## Key Dependencies

- **Django 5.2.6** - Web framework
- **djangorestframework** - API framework
- **newspaper3k** - Article content scraping
- **openai** - AI summarization service
- **streamlit** - Frontend web app
- **requests** - HTTP client
- **beautifulsoup4** - HTML parsing
- **python-dotenv** - Environment variable management

## Data Flow

1. User enters topic in Streamlit frontend
2. Frontend sends POST request to Django API (`/api/news/`)
3. Backend validates topic using OpenAI
4. Backend fetches articles from NewsAPI
5. Backend scrapes full article content using newspaper3k
6. Backend combines and truncates text content
7. Backend generates summary using OpenAI
8. Backend returns summary and articles to frontend
9. Frontend displays summary and top 5 articles with links

## API Endpoints

- `POST /api/news/` - Main endpoint for news summarization
  - Request: `{"topic": "string"}`
  - Response: `{"summary": "string", "articles": [...]}`

## Environment Configuration

The project uses environment variables stored in `.env`:
- `OPENAI_API_KEY` - Required for topic validation and summarization
- `NEWS_API_KEY` - Required for fetching articles from NewsAPI

## Database

- Uses SQLite3 as default database (`db.sqlite3`)
- No custom models currently defined in `news/models.py`