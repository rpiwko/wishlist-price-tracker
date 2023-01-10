"""
Module to find prices on nexto.pl
"""


from ..html_downloader import requests as html_downloader
from .base_shop import base_shop


class nexto(base_shop):

    def get_supported_domain(self):
        return "nexto.pl"


    def get_the_price(self, url):
        return self._find_price(html_downloader.get_the_html(url))


    def get_prices(self, url_list):
        urls_with_prices = {}
        urls_with_htmls = html_downloader.get_htmls(url_list)
        for url in urls_with_htmls:
            try:
                urls_with_prices[url] = self._find_price(urls_with_htmls[url])
            except Exception as e:
                logging.error(f"Unable to extract price from HTML for URL='{url}' because of error:\n{str(e)}")
                urls_with_prices[url] = None
        return urls_with_prices


    def _find_price(self, html):
        """
        Get the price from HTML

        Args:
            html (obj): BeautifulSoup object parsed with html.parser

        Returns:
            Raw price text extracted from HTML which may contain some garbage and formatting characters
            None if html was None
        """
        if html:
            price_tag = html.find_all("div", class_="prices")
            assert len(price_tag) == 1, f"Expected one <prices> tag but getting {len(price_tag)}"
            price_string = price_tag[0].find("strong", class_="price").get_text()
            return price_string
