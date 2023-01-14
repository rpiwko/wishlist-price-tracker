"""
Base class for shops with static pages
"""


import logging
from ..html_downloader import requests as html_downloader


class base_static_page_shop:

    def get_supported_domain(self):
        raise NotImplementedError("The get_supported_domain() method needs to be overridden in each class which inherits from base_static_page_shop!")


    def get_the_price(self, url):
        """
        Gets the price from single URL. The _find_price_in_html() method needs to be overridden 
        in each class which inherits from base_static_page_shop

        Args:
            url(str): URL to nexto.pl web store item

        Returns:
            url (str): Raw price text extracted from HTML which may contain some garbage and formatting characters
        """
        return self._find_price_in_html(html_downloader.get_the_html(url))


    def get_prices(self, url_list):
        """
        Get the price from multiple URLs

        Args:
            url_list: list of URLs to get the prices from

        Returns:
            Dictonary with URLs and raw price texts: 
            {"url1": "raw_price_text1", "url2": "raw_price_text2", "url3": "raw_price_text3"...}
        """
        urls_with_prices = {}
        urls_with_htmls = html_downloader.get_htmls(url_list)
        for url in urls_with_htmls:
            try:
                urls_with_prices[url] = self._find_price_in_html(urls_with_htmls[url])
            except Exception as e:
                logging.error(f"Unable to extract price from HTML for URL='{url}' because of error:\n{str(e)}")
                urls_with_prices[url] = None
        return urls_with_prices


    def _find_price_in_html(self, html):
        """
        Get the price from HTML. This method needs to be overridden in each class which inherits from base_dynamic_page_shop

        Args:
            html (obj): BeautifulSoup object parsed with html.parser

        Returns:
            Raw price text extracted from HTML which may contain some garbage and formatting characters
            None if html was None
        """
        raise NotImplementedError("The _find_price_in_html() method needs to be overridden in each class which inherits from base_static_page_shop!")
