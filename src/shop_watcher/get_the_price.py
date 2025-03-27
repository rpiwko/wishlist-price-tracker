"""
Get the price from single URL
"""


import logging
from shop_watcher import domains_manager
from shop_watcher import string_tools
import shop_watcher


domains_manager.import_shop_modules()


def get_the_price(url):
    """
    Get the price from single URL

    Args:
        url (str): URL to get the price from

    Returns:
        Tuple with price extracted from URL as valid float number and availability flag. 
        Availability flag values:
        - True - item is available
        - False - item is not available anymore
    """
    logging.info("Getting the price for URL: " + url)
    domain = string_tools.get_domain_from_url(url)
    domains_manager.validate_domain(domain)
    shop_module = domains_manager.get_shop_module_for_domain(domain)
    logging.info("Module to use: " + shop_module)
    raw_price_string, is_available = _execute_get_the_price_from_shop_module(shop_module, url)
    try:
        valid_price_string = string_tools.format_and_validate_the_price(raw_price_string)
    except Exception as e:
        logging.error(f"Unable to get valid price for URL={url} because of error: {str(e)}")
        valid_price_string = None
    return [valid_price_string, is_available]


def _execute_get_the_price_from_shop_module(shop_module, url):
    """
    Executes get_the_price() method from target shop module

    Args:
        shop_module (str): target shop module to execute the get_the_price() method from
        url (str): URL to get the price from, passed to get_the_price()
    
    Returns:
        Tuple with raw price text extracted from HTML and availability flag
    """
    module_class = shop_module.rsplit('.', 1)[-1]
    raw_price_string_with_availability_flag = eval(f"{shop_module}.{module_class}().get_the_price('{url}')")
    return raw_price_string_with_availability_flag

