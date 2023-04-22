from tech_news.database import search_news
from datetime import date


def search_by_title(title):
    query = {"title": {"$regex": title, "$options": "i"}}
    return [(news["title"], news["url"]) for news in search_news(query)]


def search_by_date(date_str):
    try:
        formatted_date = date.fromisoformat(date_str)
        formatted_date = formatted_date.strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")

    query = search_news({"timestamp": formatted_date})
    return [(news["title"], news["url"]) for news in query]


def search_by_category(category):
    query = search_news({"category": {"$regex": category, "$options": "i"}})
    return [(news["title"], news["url"]) for news in query]
