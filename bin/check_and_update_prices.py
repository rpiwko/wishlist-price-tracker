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
results = shop_watcher.get_the_price("https://www.nexto.pl/ebooki/hobbit,_czyli_tam_i_z_powrotem_p1249864.xml")
print("nexto.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://www.nexto.pl/ebooki/zbyt_wielcy_by_upasc_p34300.xml")
print("nexto.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.planszomania.pl/karciane/4983/Marvel-Legendary:-Deck-Building-Game.html")
print("planszomania.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://www.planszomania.pl/strategiczne/25596/Black-Rose-Wars-edycja-podstawowa.html")
print("planszomania.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://virtualo.pl/ebook/hobbit-czyli-tam-i-z-powrotem-i360890/")
print("virtualo.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://virtualo.pl/ebook/biala-bluzka-i7148/")
print("virtualo.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.publio.pl/hobbit-j-r-r-tolkien,p87958.html")
print("publio.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://www.publio.pl/opowiadania-wszystkie-leopold-tyrmand,p70957.html")
print("publio.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://ebookpoint.pl/ksiazki/po-pismie-jacek-dukaj,e_12my.htm#format/e")
print("ebookpoint.pl - available item w promo: " + str(results))
results = shop_watcher.get_the_price("https://ebookpoint.pl/ksiazki/powierniczka-opowiesci-sally-page,e_2xk9.htm")
print("ebookpoint.pl - available item w/o promo: " + str(results))
results = shop_watcher.get_the_price("https://ebookpoint.pl/ksiazki/spiacy-giganci-sylvain-neuvel,e_0b1m.htm#format/e")
print("ebookpoint.pl - not available item: " + str(results))

print("")
print("##### Test get_prices()")
dir_path = Path(Path(__file__).parent.joinpath("../etc")).resolve()
urls_with_files = json_manager.get_offers_urls(dir_path)
logging.info("Found URLs:\n" + str(urls_with_files))

urls_with_prices_and_availability = shop_watcher.get_prices(urls_with_files.keys())
print(urls_with_prices_and_availability)

json_manager.update_prices(urls_with_files, urls_with_prices_and_availability)
