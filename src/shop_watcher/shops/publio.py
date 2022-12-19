"""
Module to find price on publio.pl
"""


import logging
from bs4 import BeautifulSoup
from ..html_downloader import selenium as html_downloader


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
    price = _find_price(html_downloader.get_the_html(url, element_to_wait="//div[@class='prices']"))
    return price


def get_prices(url_list):
    urls_with_prices = {}
    urls_with_htmls = html_downloader.get_htmls(url_list, element_to_wait="//div[@class='prices']")
    for url in urls_with_htmls:
        urls_with_prices[url] = _find_price(urls_with_htmls[url])
    return urls_with_prices


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
