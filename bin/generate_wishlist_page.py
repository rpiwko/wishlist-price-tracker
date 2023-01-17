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

log_files_dir = Path(__file__).parent.joinpath("../logs")
initialize_logging(log_files_dir, __file__)

logging.info("****************************************************************")
logging.info("*************************** Starting ***************************")
logging.info("")

etc_dir_path = Path(Path(__file__).parent.joinpath("../etc")).resolve()
wishlist_items = json_manager.read_jsons_from_files(etc_dir_path)
logging.info("Found items:\n" + str(wishlist_items))
html_table = html_builder.build_table_from_objects(wishlist_items)

template_file = Path.joinpath(etc_dir_path, "page_template.html")
output_file = Path.joinpath(Path.home(), "Desktop/my_wishlist.html")
html_builder.put_table_into_html_page(html_table, template_file, "{{WISHLIST_ITEMS_TABLE}}", output_file)
