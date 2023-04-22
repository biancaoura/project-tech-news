import requests
from time import sleep
from parsel import Selector
from tech_news.database import create_news


def fetch(url):
    sleep(1)
    try:
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def scrape_updates(html_content):
    selector = Selector(text=html_content)
    return selector.css(".entry-title a::attr(href)").getall()


def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    return selector.css(".next ::attr(href)").get()


def scrape_news(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel='canonical']::attr(href)").get()
    title = selector.css(".entry-title::text").get().strip()
    timestamp = selector.css(".meta-date::text").get()
    writer = selector.css(".meta-author span.author a::text").get()
    reading_time = selector.css(".meta-reading-time::text").get().split()[0]
    summary = "".join(
        selector.css(".entry-content > p:nth-of-type(1) *::text").getall()
    ).strip()
    category = selector.css(".category-style .label::text").get()

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": int(reading_time),
        "summary": summary,
        "category": category,
    }


def get_tech_news(amount):
    page_url = fetch("https://blog.betrybe.com/")
    links = scrape_updates(page_url)

    while len(links) < amount:
        next_page = scrape_next_page_link(page_url)
        page_url = fetch(next_page)
        news_links = scrape_updates(page_url)
        for news_link in news_links:
            links.append(news_link)

    news_list = [scrape_news(fetch(link)) for link in links[:amount]]

    create_news(news_list)

    return news_list
