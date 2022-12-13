"""
Module to find price on publio.pl
"""


import logging
from bs4 import BeautifulSoup
from ..html_parsers import selenium as download_component


def get_supported_domain():
    return "publio.pl"


def get_the_price(url):
    """
    Gets the price from URL

    Args:
        url(str): URL to publio.pl web store item

    Returns:
        url (str): 
    """
    logging.info("Getting price for URL: " + url)
    price = _find_price(download_component.get_the_html(url))
    return price


def _find_price(html):
    """
    Get the price from HTML

    Args:
        html (obj): BeautifulSoup object parsed with html.parser

    Returns:
        Raw price text extracted from HTML which may contain some garbage and formatting characters
    """
    price_tag = html.find_all("div", class_="prices")
    assert len(price_tag) == 1, f"Expected one <prices> tag but getting {len(price_tag)}"
    price_string = price_tag[0].find("div", class_="current").get_text()
    return price_string
