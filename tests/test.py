import pytest
from dputils.scrape import Scraper, Tag

class TestScrapeModule:
    @pytest.fixture
    def scraper(self):
        url = "https://www.example.com"
        return Scraper(url)

    @pytest.fixture
    def title_tag(self):
        return Tag(name='h1', cls='title', output='text')

    @pytest.fixture
    def price_tag(self):
        return Tag(name='span', cls='price', output='text')

    def test_get_data_from_page(self, scraper, title_tag, price_tag):
        data = scraper.get_data_from_page(title=title_tag, price=price_tag)
        assert isinstance(data, dict)
        assert 'title' in data
        assert 'price' in data

    def test_get_repeating_data_from_page(self, scraper):
        target_tag = Tag(name='div', cls='product-list')
        item_tag = Tag(name='div', cls='product-item')
        title_tag = Tag(name='h2', cls='product-title', output='text')
        price_tag = Tag(name='span', cls='product-price', output='text')
        link_tag = Tag(name='a', cls='product-link', output='href')

        products = scraper.get_repeating_data_from_page(
            target=target_tag,
            items=item_tag,
            title=title_tag,
            price=price_tag,
            link=link_tag
        )

        assert isinstance(products, list)
        for product in products:
            assert isinstance(product, dict)
            assert 'title' in product
            assert 'price' in product
            assert 'link' in product