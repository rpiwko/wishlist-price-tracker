"""
Module to find prices on virtualo.pl
"""


import logging
from bs4 import BeautifulSoup
from ..html_downloader import requests as html_downloader


def get_supported_domain():
    return "virtualo.pl"


def get_the_price(url):
    """
    Gets the price from single URL

    Args:
        url(str): URL to virtualo.pl web store item

    Returns:
        url (str): Raw price text extracted from HTML which may contain some garbage and formatting characters
    """
    return _find_price(html_downloader.get_the_html(url))


def get_prices(url_list):
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
    price_tag = html.find_all("div", class_="price-main")
    assert len(price_tag) == 1, f"Expected one <price-main> tag but getting {len(price_tag)}"
    price_string = price_tag[0].find("span", itemprop="price").get_text()
    return price_string
