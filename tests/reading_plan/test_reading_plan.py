from tech_news.analyzer.reading_plan import ReadingPlanService
from unittest.mock import MagicMock
import pytest


mock = [
    {
        "url": "https://blog.betrybe.com/mock/dog-ai",
        "title": "Dog AI",
        "timestamp": "03/04/2023",
        "writer": "Mr Woof",
        "reading_time": 20,
        "summary": "First AI created by a dog",
        "category": "Technology",
    },
    {
        "url": "https://blog.betrybe.com/mock/cat-astronaut",
        "title": "Cat Astronaut",
        "timestamp": "04/04/2023",
        "writer": "Meow Jr.",
        "reading_time": 5,
        "summary": "History of cats in the outer space",
        "category": "Space",
    },
]


def test_reading_plan_group_news():
    ReadingPlanService._db_news_proxy = MagicMock(return_value=mock)

    with pytest.raises(
        ValueError, match="'available_time' deve ser maior que zero"
    ):
        ReadingPlanService.group_news_for_available_time(-1)

    news = ReadingPlanService.group_news_for_available_time(11)

    assert len(news["readable"]) == 1
    assert len(news["unreadable"]) == 1

    if len(news["readable"]) > 0:
        assert news["readable"][0]["unfilled_time"] == 6
