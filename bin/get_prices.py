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


print("##### Test get_the_price()")
print(shop_watcher.get_the_price("https://www.nexto.pl/ebooki/do_cna_p1306641.xml"))

print()
print("##### Test get_prices()")
dir_path = Path(Path(__file__).parent.joinpath("../etc")).resolve()
urls_with_files = json_manager.get_offers_urls(dir_path)
logging.info("Found URLs:\n" + str(urls_with_files))

urls_with_prices = shop_watcher.get_prices(urls_with_files.keys())
print(urls_with_prices)

json_manager.update_prices(urls_with_files, urls_with_prices)


