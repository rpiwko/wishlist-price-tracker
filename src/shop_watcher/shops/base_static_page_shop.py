"""
Base class for shops with static pages
"""


import logging
from ..html_downloader import requests as html_downloader


class base_static_page_shop:

    def get_supported_domain(self):
        raise NotImplementedError("The get_supported_domain() method needs to be \
overridden in each class which inherits from base_static_page_shop!")

    def get_the_price(self, url):
        """
        Gets the price from single URL. The _find_price_in_html() method needs to be overridden 
        in each class which inherits from base_static_page_shop

        Args:
            url(str): URL to web store item

        Returns:
            url (str): Tuple with raw price text extracted from HTML and availability flag
        """
        bs_html = html_downloader.get_the_html(url)
        raw_price_string, is_available = self._get_price_and_availability_from_html(bs_html)
        return raw_price_string, is_available

    def get_prices(self, url_list):
        """
        Get the price from multiple URLs

        Args:
            url_list: list of URLs to get the prices from

        Returns:
            Dictionary with URLs, raw price texts and availability flags:
            {"url1": ["raw_price_text1", True], "url2": ["raw_price_text2", True], "url3": ["raw_price_text3", False]...}
        """
        urls_with_prices = {}
        urls_with_htmls = html_downloader.get_htmls(url_list)
        for url in urls_with_htmls:
            logging.info("Searching price and availability in HTML for URL=" + url)
            try:
                urls_with_prices[url] = self._get_price_and_availability_from_html(urls_with_htmls[url])
            except Exception as e:
                logging.error(f"Unable to extract price from HTML for URL='{url}' because of error: {str(e)}")
                urls_with_prices[url] = None
        return urls_with_prices

    def _get_price_and_availability_from_html(self, html):
        """
        Get the price and availability flag from HTML. 
        This method needs to be overridden in each class which inherits from base_dynamic_page_shop

        Args:
            html (obj): BeautifulSoup object parsed with html.parser

        Returns:
            Raw price text extracted from HTML which may contain some garbage and formatting characters
            None if html was None
        """
        raise NotImplementedError("The _get_price_and_availability_from_html() method needs to be \
overridden in each class which inherits from base_static_page_shop!")
