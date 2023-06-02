"""
Main script to generate wishlist HTML page
"""


import logging
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.joinpath("../src")))
from logging_setup import initialize_logging
import json_manager
import html_builder


print("Script started...")

bin_dir_path = Path(__file__).parent
log_files_dir = bin_dir_path.joinpath("../logs")
initialize_logging(log_files_dir, __file__)

logging.info("****************************************************************")
logging.info("*************************** Starting ***************************")
logging.info("")

etc_dir_path = Path(Path(__file__).parent.joinpath("../etc")).resolve()
wishlist_items = json_manager.read_jsons_from_files(etc_dir_path)
logging.info("Found items:\n" + str(wishlist_items))
html_category_selector = html_builder.build_category_selector(wishlist_items)
html_wishlist_items_table = html_builder.build_wishlist_items_table(wishlist_items)

template_file = Path.joinpath(etc_dir_path, "page_template.html")
output_file = Path.joinpath(bin_dir_path.joinpath("../out/my_wishlist.html"))
html_builder.put_element_into_template(html_category_selector, template_file, "{{CATEGORIES_SELECTOR}}", output_file)
html_builder.put_element_into_template(html_wishlist_items_table, output_file, "{{WISHLIST_ITEMS_TABLE}}", output_file)
