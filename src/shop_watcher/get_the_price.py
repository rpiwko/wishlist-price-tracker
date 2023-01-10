"""
Get the price from single URL
"""


import logging
from shop_watcher import domains_manager
from shop_watcher import string_tools
import shop_watcher


def get_the_price(url):
    """
    Get the price from single URL

    Args:
        url (str): URL to get the price from

    Returns:
        Price extracted from URL as valid float number
    """
    logging.info("Getting the price for URL: " + url)
    domains_manager.validate_domain(url)
    shop_module = domains_manager.supported_domains[string_tools.get_domain_from_url(url)]
    logging.info("Module to use: " + shop_module)
    raw_price_string = _execute_get_the_price_from_shop_module(shop_module, url)
    return string_tools.format_and_validate_the_price(raw_price_string)


def _execute_get_the_price_from_shop_module(shop_module, url):
    """
    Executes get_the_price() method from target shop module

    Args:
        shop_module (str): target shop module to execute the get_the_price() method from
        url (str): URL to get the price from, passed to get_the_price()
    
    Returns:
        Raw price text extracted from HTML which may contain some garbage and formatting characters
    """
    namespace_for_exec = dict()
    exec(f"price = shop_watcher.shops.{shop_module}.{shop_module}().get_the_price('{url}')", globals(), namespace_for_exec)
    return namespace_for_exec["price"]

