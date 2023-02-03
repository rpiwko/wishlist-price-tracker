"""
Main script to download the latest prices and generate result HTML page
"""

import logging
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.joinpath("../src")))
from logging_setup import initialize_logging
import shop_watcher as shop_watcher
import json_manager
import html_builder


print("Script started...")

log_files_dir = Path(__file__).parent.joinpath("../logs").resolve()
etc_dir_path = Path(Path(__file__).parent.joinpath("../etc")).resolve()

template_file = Path.joinpath(etc_dir_path, "page_template.html")
output_file = Path.joinpath(Path.home(), "Desktop/my_wishlist.html")

initialize_logging(log_files_dir, __file__)
logging.info("****************************************************************")
logging.info("*************************** Starting ***************************")
logging.info("")

print("##### STEP 1: Checking latest prices...")
logging.info("##### STEP 1: Checking latest prices...")

urls_with_files = json_manager.get_offers_urls(etc_dir_path)
logging.info("Found URLs:\n" + str(urls_with_files))

print(f"Total number of URLs to process: {len(urls_with_files)}")
urls_with_prices_and_availability = shop_watcher.get_prices(urls_with_files.keys(), show_progress_bar=True)
json_manager.update_prices(urls_with_files, urls_with_prices_and_availability)

print("Checking prices complete!")
logging.info("Checking prices complete!")

print("##### STEP 2: Generating result HTML page...")
logging.info("##### STEP 2: Generating result HTML page...")

wishlist_items = json_manager.read_jsons_from_files(etc_dir_path)
logging.info("Found items:\n" + str(wishlist_items))
html_category_selector = html_builder.build_category_selector(wishlist_items)
html_wishlist_items_table = html_builder.build_wishlist_items_table(wishlist_items)

html_builder.put_element_into_template(html_category_selector, template_file, "{{CATEGORIES_SELECTOR}}", output_file)
html_builder.put_element_into_template(html_wishlist_items_table, output_file, "{{WISHLIST_ITEMS_TABLE}}", output_file)

print("Generating result HTML page complete!")
logging.info("Generating result HTML page complete!")

logging.info("")
logging.info("**************** Script successfully completed! ****************")
logging.info("****************************************************************")
logging.info("")