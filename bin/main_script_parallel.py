"""
Main script to download the latest prices and generate result HTML page.
Download process is done in parallel, in multiple threads
"""

import logging
import sys
import queue
import concurrent.futures
from threading import Thread
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.joinpath("../src")))
from logging_setup import initialize_logging
import shop_watcher as shop_watcher
import json_manager
import html_builder


def _flush_results_to_files():
    logging.info("Queue monitoring was started")
    is_end_of_queue_found = False
    while not is_end_of_queue_found:
        new_entry = domains_with_prices_and_availability_queue.get(True)
        if new_entry is not None:
            logging.info(f"New items were found in queue (count={len(new_entry)}). About to start updating files...")
            json_manager.update_prices(urls_with_files, new_entry)
        else:
            logging.info("End of queue signal was received. Queue monitoring is about to stop...")
            is_end_of_queue_found = True
    logging.info("Queue monitoring was stopped")


def _get_prices_for_domain(domain):
    domains_with_prices_and_availability_queue.put(shop_watcher.get_prices(urls_grouped_by_domains[domain]))


def group_urls_by_domain(urls):
    urls_by_domains = {}
    for url in urls:
        domain = shop_watcher.string_tools.get_domain_from_url(url)
        if domain not in urls_by_domains.keys():
            urls_by_domains[domain] = list()
        urls_by_domains[domain].append(url)
    return urls_by_domains


print("Script started...")

bin_dir_path = Path(__file__).parent
etc_dir_path = Path(bin_dir_path.joinpath("../etc")).resolve()
log_files_dir = bin_dir_path.joinpath("../logs").resolve()

page_template_file = Path.joinpath(etc_dir_path, "page_template.html")
page_output_file = Path.joinpath(bin_dir_path.joinpath("../out/my_wishlist.html"))

initialize_logging(log_files_dir, __file__)
logging.info("****************************************************************")
logging.info("*************************** Starting ***************************")
logging.info("")

print("##### STEP 1: Checking latest prices...")
logging.info("##### STEP 1: Checking latest prices...")

urls_with_files = json_manager.get_offers_urls(etc_dir_path)
logging.info("Found URLs:\n" + str(urls_with_files))

print(f"Total number of URLs to process: {len(urls_with_files)}")

# Prepare queue worker
domains_with_prices_and_availability_queue = queue.Queue()
files_updater = Thread(target=_flush_results_to_files)
files_updater.start()

# Split found URLs by domain
urls_grouped_by_domains = group_urls_by_domain(urls_with_files.keys())
logging.debug(f"urls_grouped_by_domains={urls_grouped_by_domains}")

# Actual prices gathering
with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls_grouped_by_domains.keys())) as executor:
    executor.map(_get_prices_for_domain, urls_grouped_by_domains)

domains_with_prices_and_availability_queue.put(None) # signal for files_updater to quit
files_updater.join()

print("Checking prices complete!")
logging.info("Checking prices complete!")

print("##### STEP 2: Generating result HTML page...")
logging.info("##### STEP 2: Generating result HTML page...")

wishlist_items = json_manager.read_jsons_from_files(etc_dir_path)
logging.info("Found items:\n" + str(wishlist_items))
html_category_selector = html_builder.build_category_selector(wishlist_items)
html_wishlist_items_table = html_builder.build_wishlist_items_table(wishlist_items)

html_builder.put_element_into_template(html_category_selector, page_template_file, "{{CATEGORIES_SELECTOR}}", page_output_file)
html_builder.put_element_into_template(html_wishlist_items_table, page_output_file, "{{WISHLIST_ITEMS_TABLE}}", page_output_file)

print("Generating result HTML page complete!")
logging.info("Generating result HTML page complete!")

logging.info("")
logging.info("**************** Script successfully completed! ****************")
logging.info("****************************************************************")
logging.info("")
