
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


def get_prices(url_list):
    groupped_urls = _group_urls_by_domain(url_list)
    urls_with_prices = {}
    for domain in groupped_urls:
        logging.info("Getting prices for domain: " + domain)
        shop_module = supported_domains[domain]
        logging.info("Module to use: " + shop_module)
        domain_urls_with_prices = _execute_get_prices_from_shop_module(shop_module, groupped_urls[domain])
        for url in domain_urls_with_prices:
            try:
                urls_with_prices[url] = string_tools.format_and_validate_the_price(domain_urls_with_prices[url])
            except ValueError as e:
                logging.info(f"Unable to get valid price for URL='{url}': {str(e)}")
                urls_with_prices[url] = None
        
    return urls_with_prices


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


def _execute_get_prices_from_shop_module(module, url_list):
    namespace_for_exec = dict()
    exec(f"price = {module}.get_prices({url_list})", globals(), namespace_for_exec)
    return namespace_for_exec["price"]


def _group_urls_by_domain(url_list):
    grouped_urls = {}
    for url in url_list:
        try:
            _validate_domain(url)
            url_domain = string_tools.get_domain_from_url(url)
            if url_domain not in grouped_urls:
                grouped_urls[url_domain] = [url]
            else:
                grouped_urls[url_domain].append(url)
        except ValueError as e:
            logging.error(str(e))
            logging.error("Skipping URL: " + url)
    return grouped_urls
