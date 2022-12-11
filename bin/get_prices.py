"""
Main script to download latest prices
"""


import logging
from pathlib import Path
from datetime import datetime
import sys
sys.path.append(str(Path(__file__).resolve().parent.joinpath("..")))
import src.price_getters.virtualo as virtualo_price_getter


print("Script started...")

# Logger elements
log_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
root_logger = logging.getLogger()
log_files_dir = Path(__file__).parent.joinpath("../logs")
log_file_name = Path(__file__).stem + "_" + datetime.now().strftime("%Y%m%d_%H%M%S")

logging.debug("") # warm up to initialize logger handlers
default_console_handler = root_logger.handlers[0]
log_file_handler = logging.FileHandler(Path(log_files_dir, log_file_name).with_suffix(".log"))
log_file_handler.setFormatter(log_formatter)
root_logger.addHandler(log_file_handler)
root_logger.setLevel(logging.INFO)
root_logger.removeHandler(default_console_handler)  # do not propagate logs to console

logging.info("****************************************************************")
logging.info("*************************** Starting ***************************")
logging.info("")

urls = ["https://virtualo.pl/ebook/hobbit-czyli-tam-i-z-powrotem-i360890/",
        "https://www.nexto.pl/ebooki/oliver_twist_p1136542.xml"]

for url in urls:
    price = virtualo_price_getter.get_the_price(url)
    print("Found price is " + str(price))
