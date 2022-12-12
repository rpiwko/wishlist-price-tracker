"""
Module to find price on publio.pl
"""


import logging
from bs4 import BeautifulSoup
import src.common.selenium_downloader as selenium_downloader
import src.common.string_tools as string_tools


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
    _validate_url(url)
    price = _find_price(selenium_downloader.get_the_html(url))
    price = string_tools.format_and_validate_the_price(price)
    return price


def _validate_url(url):
    """
    Checks whether URL is supported by this price getter

    Args:
        url (str): URL to validate
    """
    url_domain = string_tools.get_domain_from_url(url)
    if url_domain == get_supported_domain():
        pass
    else:
        raise ValueError(f"Unexpected URL domain detected: '{url_domain}'. Should be: {get_supported_domain()}")


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
