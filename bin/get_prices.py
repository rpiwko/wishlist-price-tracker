"""
Main script to download latest prices
"""


import logging
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.joinpath("../src")))
from logging_setup import initialize_logging
import shop_watcher as shop_watcher
import json_manager as json_manager


print("Script started...")

log_files_dir = Path(__file__).parent.joinpath("../logs")
initialize_logging(log_files_dir, __file__)

logging.info("****************************************************************")
logging.info("*************************** Starting ***************************")
logging.info("")


dir_path = Path("./etc/").resolve()
urls = json_manager.get_offers_urls(dir_path)
logging.info("Found URLs:\n" + str(urls))

for url in urls:
    try:
        current_price = shop_watcher.get_the_price(url)
        json_manager.update_price(urls[url], url, current_price)
    except Exception as e:
        logging.error(f"Error occurred while processing {url}:\n{str(e)}")
