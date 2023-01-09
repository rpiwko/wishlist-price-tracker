"""
Module to find prices on publio.pl
"""


import logging
from bs4 import BeautifulSoup
from ..html_downloader import selenium as html_downloader


def get_supported_domain():
    return "publio.pl"


def get_the_price(url):
    """
    Gets the price from single URL

    Args:
        url(str): URL to publio.pl web store item

    Returns:
        url (str): Raw price text extracted from HTML which may contain some garbage and formatting characters
    """
    price = _find_price(html_downloader.get_the_html(url, element_to_wait="//div[@class='prices']"))
    return price


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
    urls_with_htmls = html_downloader.get_htmls(url_list, element_to_wait="//div[@class='prices']")
    for url in urls_with_htmls:
        try:
            urls_with_prices[url] = _find_price(urls_with_htmls[url])
        except Exception as e:
            logging.error(f"Unable to extract price from HTML for URL='{url}' because of error:\n{str(e)}")
            urls_with_prices[url] = None
    return urls_with_prices


def _find_price(html):
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
        price_string = price_tag[0].find("div", class_="current").get_text()
        return price_string
