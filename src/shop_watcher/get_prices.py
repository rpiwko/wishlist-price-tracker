"""
Get prices from multiple URLs
"""


import logging
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from shop_watcher import domains_manager
from shop_watcher import string_tools
import shop_watcher


domains_manager.import_shop_modules()


def get_prices(url_list, show_progress_bar=False, parallel=False):
    """
    Get the price from multiple URLs

    Args:
        url_list: list of URLs to get the prices from
        show_progress_bar: when True, then progress bar will be printed to output
        parallel: when True, then each domain will be processed in separate thread

    Returns:
        Dictionary with URLs, prices as valid float numbers and availability flags:
        {"url1": [12.34, True], "url2": [56.78, True], "url3": [None, False], "url4": [99.99, False]...}
        If price could not be extracted from URL, then appropriate error is logged and price is set to None
    """

    urls_grouped_by_domain = _group_urls_by_domain(url_list)
    urls_with_prices = {}
    processed_urls_cnt = 0
    if show_progress_bar:
        _print_progress_bar(processed_urls_cnt, len(url_list))

    def merge_results_and_print_progress(new_results):
        nonlocal processed_urls_cnt
        nonlocal urls_with_prices
        urls_with_prices = {**urls_with_prices, **new_results}
        completed_domain = string_tools.get_domain_from_url(list(new_results.keys())[0])
        processed_urls_cnt += len(urls_grouped_by_domain[completed_domain])
        if show_progress_bar:
            _print_progress_bar(processed_urls_cnt, len(url_list))
        else:
            progress = "{0:.1f}".format(100 * (processed_urls_cnt / len(url_list)))
            print(f"Getting prices for {completed_domain} completed! Total progress: {progress}%")

    if parallel:
        with ThreadPoolExecutor(max_workers=len(urls_grouped_by_domain.keys())) as executor:
            futures = [executor.submit(_get_prices_for_domain, urls) for urls in urls_grouped_by_domain.values()]
            for future in as_completed(futures):
                merge_results_and_print_progress(future.result())
    else:
        for domain in urls_grouped_by_domain:
            merge_results_and_print_progress(_get_prices_for_domain(urls_grouped_by_domain[domain]))

    if processed_urls_cnt != len(url_list):
        print()
        print(f"Number of skipped URLs: {len(url_list) - processed_urls_cnt}. Check logs for more details")
        logging.warning(f"Number of skipped URLs: {len(url_list) - processed_urls_cnt}. Check logs for more details")
    return urls_with_prices


def _get_prices_for_domain(url_list):
    """
    Get prices from URLs in single domain. If url_list contains URLs from more than one domain, then ValueError
    is raised

    Args:
        url_list: list of URLs to get the prices from

    Returns:
        Dictionary with URLs, prices as valid float numbers and availability flags:
        {"url1": [12.34, True], "url2": [56.78, True], "url3": [None, False], "url4": [99.99, False]...}
    """
    if url_list:
        domain = string_tools.get_domain_from_url(url_list[0])
        logging.info(f"[{domain}] Getting prices for {domain} started")
        shop_module = domains_manager.get_shop_module_for_domain(domain)
        logging.info(f"[{domain}] Module to use: {shop_module}")
        urls_with_prices = _execute_get_prices_from_shop_module(shop_module, url_list)
        for url in url_list:
            assert string_tools.get_domain_from_url(url) == domain, \
                "Two different domains detected in url_list parameter!"
            if urls_with_prices[url]:
                try:
                    logging.info(f"[{domain}] Formatting and validating price found under URL={url}")
                    valid_price_string = string_tools.format_and_validate_the_price(urls_with_prices[url][0])
                    urls_with_prices[url] = valid_price_string, urls_with_prices[url][1]
                except ValueError as e:
                    logging.error(f"[{domain}] Price formatting failed for URL='{url}': {str(e)}")
                    urls_with_prices[url] = None, urls_with_prices[url][1]
            else:
                urls_with_prices[url] = None, None
        logging.info(f"[{domain}] Getting prices for {domain} completed!")
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
    logging.info("Grouping URLs by domain started")
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
            logging.error(f"Skipping URL='{url}' because of exception: {str(e)} ")
    logging.info("Grouping URLs by domain completed")
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
