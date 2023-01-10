"""
Base class for shops
"""


import logging
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class base_shop(ABC):

    @abstractmethod
    def get_supported_domain(self):
        pass

    @abstractmethod
    def get_the_price(self, url):
        """
        Gets the price from single URL

        Args:
            url(str): URL to nexto.pl web store item

        Returns:
            url (str): Raw price text extracted from HTML which may contain some garbage and formatting characters
        """
        pass

    @abstractmethod
    def get_prices(self, url_list):
        """
        Get the price from multiple URLs

        Args:
            url_list: list of URLs to get the prices from

        Returns:
            Dictonary with URLs and raw price texts: 
            {"url1": "raw_price_text1", "url2": "raw_price_text2", "url3": "raw_price_text3"...}
        """
        pass

