"""
Get prices from multiple URLs
"""


import logging
from shop_watcher import domains_manager
from shop_watcher import string_tools
import shop_watcher


domains_manager.import_shop_modules()


def get_prices(url_list, show_progress_bar=False):
    """
    Get the price from multiple URLs

    Args:
        url_list: list of URLs to get the prices from
        show_progress_bar: when True, then progress bar will be printed to output

    Returns:
        Dictionary with URLs, prices as valid float numbers and availability flags:
        {"url1": [12.34, True], "url2": [56.78, True], "url3": [None, False], "url4": [99.99, False]...}
        If price could not be extracted from URL, then appropriate error is logged and price is set to None
    """
    grouped_urls = _group_urls_by_domain(url_list)
    urls_with_prices = {}
    processed_urls_cnt = 0
    if show_progress_bar:
        _print_progress_bar(processed_urls_cnt, len(url_list))
    for domain in grouped_urls:
        logging.info(f"Getting prices for {domain} started")
        shop_module = domains_manager.get_shop_module_for_domain(domain)
        logging.info("Module to use: " + shop_module)
        domain_urls_with_prices = _execute_get_prices_from_shop_module(shop_module, grouped_urls[domain])
        for url in domain_urls_with_prices:
            if domain_urls_with_prices[url]:
                try:
                    logging.info("Formatting and validating price found under URL=" + url)
                    valid_price_string = string_tools.format_and_validate_the_price(domain_urls_with_prices[url][0])
                    urls_with_prices[url] = valid_price_string, domain_urls_with_prices[url][1]
                except ValueError as e:
                    logging.error(f"Unable to get valid price for URL='{url}': {str(e)}")
                    urls_with_prices[url] = None, domain_urls_with_prices[url][1]
            else:
                urls_with_prices[url] = None, None
        logging.info(f"Getting prices for {domain} completed!")
        processed_urls_cnt += len(grouped_urls[domain])
        if show_progress_bar:
            _print_progress_bar(processed_urls_cnt, len(url_list))
        elif processed_urls_cnt > 0:
            print(f"Total progress: {processed_urls_cnt}/{len(url_list)}")
    if processed_urls_cnt != len(url_list):
        print()
        print(f"Number of skipped URLs: {len(url_list) - processed_urls_cnt}. Check logs for more details")
        logging.info(f"Number of skipped URLs: {len(url_list) - processed_urls_cnt}. Check logs for more details")
    return urls_with_prices


def _execute_get_prices_from_shop_module(shop_module, url_list):
    """
    Executes get_prices() method from target shop module

    Args:
        shop_module (str): target shop module to execute the get_prices() method from
        url_list: list of URLs to get the prices from, passed to get_prices()
    
    Returns:
        Dictionary with URLs, raw price texts and availability flags:
        {"url1": ["raw_price_text1", True], "url2": ["raw_price_text2", True], "url3": ["raw_price_text3", False]...}
    """
    namespace_for_exec = dict()
    module_class = shop_module.rsplit('.', 1)[-1]
    exec(f"urls_with_prices = {shop_module}.{module_class}().get_prices({url_list})", globals(), namespace_for_exec)
    return namespace_for_exec["urls_with_prices"]


def _group_urls_by_domain(url_list):
    """
    Groups URLs by domain. URLs belonging to not supported domains will be skipped from results

    Args:
        url_list: list of URLs to group
    
    Returns:
        Dictionary with URLs grouped by domain:
        {"domain1": ["url1", "url2"...], "domain2": ["url3", "url4"...], "domain3": ["url5", "url6"...]}
    """
    grouped_urls = {}
    for url in url_list:
        try:
            domain = string_tools.get_domain_from_url(url)
            domains_manager.validate_domain(domain)            
            if domain not in grouped_urls:
                grouped_urls[domain] = [url]
            else:
                grouped_urls[domain].append(url)
        except ValueError as e:
            logging.error("Skipping URL: " + url)
    return grouped_urls


def _print_progress_bar (iteration, total):
    length = 50
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = "█" * filled_length + "-" * (length - filled_length)
    print("\rProgress: |%s| %s%% Complete" % (bar, percent), end = "\r")
    # Print New Line on Complete
    if iteration == total:
        print()
