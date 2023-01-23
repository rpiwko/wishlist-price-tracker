"""
Module to manage json files with wishlist items
"""


import logging
import json
from datetime import datetime
from pathlib import Path
import shutil


time_format = "%Y-%m-%d %H:%M"


def read_json_from_file(file_path):
    logging.info("Reading file: " + str(file_path))
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def read_jsons_from_files(dir_path):
    items = []
    for json_file in sorted(Path(dir_path).glob("**/*.json")):
        item = read_json_from_file(json_file)
        item["jsonFile"] = json_file
        items.append(item)
    return items


def save_json_to_file(json_dict, file_path, backup_file=True):
    logging.info("Saving file: " + str(file_path))
    if backup_file:
        _make_a_backup(file_path)
    with open(file_path, "w") as json_file:
        json_file.write(json.dumps(json_dict, indent=4, ensure_ascii=False))


def get_offer_urls(file_path):
    json_dict = read_json_from_file(file_path)
    urls = []
    for offer in json_dict["offers"]:
        urls.append(offer["url"])
    return urls


def get_offers_urls(dir_path):
    logging.info("Extracting offers URLs from dir: " + str(dir_path))
    urls_with_files = {}
    for json_file in sorted(Path(dir_path).glob("**/*.json")):
        urls_in_json = get_offer_urls(json_file)
        for url in urls_in_json:
            if url in urls_with_files:
                error_text = "The same URL in two different json files is not supported:"
                error_text += "\nURL: " + url
                error_text += "\nFile1: " + str(urls_with_files[url])
                error_text += "\nFile2: " + str(json_file)
                raise KeyError(error_text)
            urls_with_files[url] = json_file
    return urls_with_files
                

def update_the_price_and_availability(file_path, url, new_price, is_available):
    json_dict = read_json_from_file(file_path)
    ts = datetime.now().strftime(time_format)
    logging.info("Updating price in file: " + str(file_path))
    logging.info("...for URL: " + str(url))
    logging.info("...with value: " + str(new_price))
    logging.info("...with TS: " + ts)
    logging.info("...and availability: " + str(is_available))
    for offer in json_dict["offers"]:
        if offer["url"] == url:
            # Updating latestPrice
            logging.info("Previous latestPrice: " + str(offer["latestPrice"]))
            logging.info("Previous latestPriceDate: " + str(offer["latestPriceDate"]))
            logging.info("Previous isAvailable: " + str(offer["isAvailable"]))
            offer["latestPrice"] = new_price
            offer["latestPriceDate"] = ts
            offer["isAvailable"] = is_available
            if new_price:
                # Updating lowestPrice
                if not offer["lowestPrice"] or offer["lowestPrice"] > new_price:
                    logging.info("Looks like this is the new lowest price")
                    logging.info("Previous lowestPrice: " + str(offer["lowestPrice"]))
                    logging.info("Previous lowestPriceDate: " + str(offer["lowestPriceDate"]))
                    offer["lowestPrice"] = new_price
                    offer["lowestPriceDate"] = ts
                # Updating highestPrice
                if not offer["highestPrice"] or offer["highestPrice"] < new_price:
                    logging.info("Looks like this is the new highest price")
                    logging.info("Previous highestPrice: " + str(offer["highestPrice"]))
                    logging.info("Previous highestPriceDate: " + str(offer["highestPriceDate"]))
                    offer["highestPrice"] = new_price
                    offer["highestPriceDate"] = ts
            save_json_to_file(json_dict, file_path)


def update_prices(urls_with_files, urls_with_prices_and_availability):
    for url in urls_with_prices_and_availability:
        try:
            new_price = urls_with_prices_and_availability[url][0]
            is_avilable = urls_with_prices_and_availability[url][1]
            update_the_price_and_availability(urls_with_files[url], url, new_price, is_avilable)
        except Exception as e:
            logging.error(f"Exception occurred while updating prices:\n{str(e)}")
            continue


def _make_a_backup(file_path):
    src = str(file_path)
    dst = src + ".BAK"
    shutil.copy(src, dst)