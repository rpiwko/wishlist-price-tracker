
import logging
import shop_watcher.string_tools as string_tools
import shop_watcher.shops.publio as publio
import shop_watcher.shops.nexto as nexto
import shop_watcher.shops.virtualo as virtualo


# TODO: Import shops dynamically, remove hardcoded supported_domains
supported_domains = {
    "nexto.pl": "nexto", 
    "publio.pl": "publio",
    "virtualo.pl": "virtualo"}


def get_the_price(url):
    logging.info("Getting the price for URL: " + url)
    _validate_domain(url)
    shop_module = supported_domains[string_tools.get_domain_from_url(url)]
    logging.info("Module to use: " + shop_module)
    raw_price_string = _execute_get_the_price_from_shop_module(shop_module, url)
    return string_tools.format_and_validate_the_price(raw_price_string)


def _validate_domain(url):
    """
    Checks whether URL domain is supported

    Args:
        url (str): URL to validate
    """
    url_domain = string_tools.get_domain_from_url(url)
    accepted_domains = list(supported_domains.keys())
    if url_domain not in accepted_domains:
        raise ValueError(f"Unexpected URL domain detected: '{url_domain}'. Accepted domains are: {accepted_domains}")


def _execute_get_the_price_from_shop_module(module, url):
    """
    Executes get_the_price() method from target shop module

    Args:
        module (str): target shop module to execute the get_the_price() method from
        url (str): URL to get the price from, passed to get_the_price()
    
    Returns:
        Raw price text extracted from HTML which may contain some garbage and formatting characters
    """
    namespace_for_exec = dict()
    exec(f"price = {module}.get_the_price('{url}')", globals(), namespace_for_exec)
    return namespace_for_exec["price"]