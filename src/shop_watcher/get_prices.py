"""
Get prices from multiple URLs
"""


import logging
import shop_watcher.domains_manager as domains_manager
import shop_watcher.string_tools as string_tools
import shop_watcher.shops.publio
import shop_watcher.shops.nexto
import shop_watcher.shops.virtualo


def get_prices(url_list):
    """
    Get the price from multiple URLs

    Args:
        url_list: list of URLs to get the prices from

    Returns:
        Dictonary with URLs and prices as valid float numbers:
        {"url1": 12.34, "url2": 56.78, "url3": None, "url4": 99.99...}
        If price could not be extracted from URL, then appropriate error is logged and price is set to None
    """
    groupped_urls = _group_urls_by_domain(url_list)
    urls_with_prices = {}
    for domain in groupped_urls:
        logging.info(f"Getting prices for {domain} started")
        shop_module = domains_manager.supported_domains[domain]
        logging.info("Module to use: " + shop_module)
        domain_urls_with_prices = _execute_get_prices_from_shop_module(shop_module, groupped_urls[domain])
        for url in domain_urls_with_prices:
            if domain_urls_with_prices[url]:
                try:
                    logging.info("Formatting and validating price found under URL=" + url)
                    urls_with_prices[url] = string_tools.format_and_validate_the_price(domain_urls_with_prices[url])
                except ValueError as e:
                    logging.error(f"Unable to get valid price for URL='{url}': {str(e)}")
                    urls_with_prices[url] = None
            else:
                urls_with_prices[url] = None
        logging.info(f"Getting prices for {domain} completed!")
    return urls_with_prices


def _execute_get_prices_from_shop_module(shop_module, url_list):
    """
    Executes get_prices() method from target shop module

    Args:
        shop_module (str): target shop module to execute the get_prices() method from
        url_list: list of URLs to get the prices from, passed to get_prices()
    
    Returns:
        Dictonary with URLs and raw price texts: 
        {"url1": "raw_price_text1", "url2": "raw_price_text2", "url3": "raw_price_text3"...}
    """
    namespace_for_exec = dict()
    exec(f"urls_with_prices = shop_watcher.shops.{shop_module}.{shop_module}().get_prices({url_list})", globals(), namespace_for_exec)
    return namespace_for_exec["urls_with_prices"]


def _group_urls_by_domain(url_list):
    """
    Groups URLs by domain

    Args:
        url_list: list of URLs to group
    
    Returns:
        Dictionary with URLs groupped by domain:
        {"domain1": ["url1", "url2"...], "domain2": ["url3", "url4"...], "domain3": ["url5", "url6"...]}
    """
    grouped_urls = {}
    for url in url_list:
        try:
            domains_manager.validate_domain(url)
            url_domain = string_tools.get_domain_from_url(url)
            if url_domain not in grouped_urls:
                grouped_urls[url_domain] = [url]
            else:
                grouped_urls[url_domain].append(url)
        except ValueError as e:
            logging.error(str(e))
            logging.error("Skipping URL: " + url)
    return grouped_urls
