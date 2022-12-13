"""
Helper module with tools for common string operations
"""

import logging
import re

def get_domain_from_url(url):
    """
    Extract domain from URL

    Args:
        url (str): URL string to extract domain from

    Returns:
        Domain string if possible (e.g. virtualo.pl), otherwise None
    """
    pattern = re.compile("((?<=https://www.)[a-z.]*|(?<=https://(?!www.))[a-z.]*)")
    domain = pattern.findall(url)
    if domain is None or len(domain) == 0 or len(domain[0]) == 0:
        return None
    else:
        return domain[0]


def format_and_validate_the_price(raw_price_string):
    """
    Converts string to float number if possible

    Args:
        price (str): string to convert

    Returns:
        Float number converted and formatted from price
    """
    logging.info("Raw price string before formatting: " + raw_price_string)
    price = str(raw_price_string).replace(",", ".").replace("zł", "").strip()
    logging.info("Price string after formatting: " + price)
    validate_the_price(price)
    return price


def validate_the_price(price):
    """
    Checks if string is valid float number greater than zero

    Args:
        price (str): price to check
    """
    if not is_valid_float_number(price):
        raise ValueError(f"Price is not a valid float number: {price}")
    if float(price) <= 0:
        raise ValueError(f"Price must be greater than zero but is: {price}")


def is_valid_float_number(str_to_check):
    """
    Checks if string can be converted to valid float number

    Args:
        str_to_check (str): string to check
    """
    try:
        float(str_to_check)
    except ValueError:
        return False
    return True
