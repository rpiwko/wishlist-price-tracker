"""
Module to manage json files with wishlist items
"""


import logging
import json
from datetime import datetime
from pathlib import Path


time_format = "%Y-%m-%d %H:%M"


def read_json_from_file(path):
    logging.info("Reading file: " + str(path))
    with open(path, "r") as json_file:
        data = json.load(json_file)
    return data


def save_json_to_file(json_dict, path):
    logging.info("Saving file: " + str(path))
    with open(path, "w") as json_file:
        json.dump(json_dict, json_file, indent=4)


def get_offer_urls(path_to_file):
    json_dict = read_json_from_file(path_to_file)
    urls = []
    for offer in json_dict["offers"]:
        urls.append(offer["url"])
    return urls


def get_offers_urls(path_to_dir):
    logging.info("Extracting offers URLs from dir: " + str(path_to_dir))
    urls_with_files = {}
    for json_file in sorted(Path(path_to_dir).glob("**/*.json")):
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
                

def update_the_price_and_availability(path, url, new_price, is_available):
    json_dict = read_json_from_file(path)
    ts = datetime.now().strftime(time_format)
    logging.info("Updating price in file: " + str(path))
    logging.info("...for URL: " + str(url))
    logging.info("...with value: " + str(new_price))
    logging.info("...with TS: " + ts)
    logging.info("...and availability: " + str(is_available))
    for offer in json_dict["offers"]:
        if offer["url"] == url:
            logging.info("Previous latestPrice: " + str(offer["latestPrice"]))
            logging.info("Previous latestPriceDate: " + str(offer["latestPriceDate"]))
            logging.info("Previous isAvailable: " + str(offer["isAvailable"]))
            offer["latestPrice"] = new_price
            offer["latestPriceDate"] = ts
            offer["isAvailable"] = is_available
            if new_price:
                # Updating lowestPrice
                if not offer["lowestPrice"] or offer["lowestPrice"] >= new_price:
                    logging.info("Looks like this is the lowest price!")
                    logging.info("Previous lowestPrice: " + str(offer["lowestPrice"]))
                    logging.info("Previous lowestPriceDate: " + str(offer["lowestPriceDate"]))
                    offer["lowestPrice"] = new_price
                    offer["lowestPriceDate"] = ts
            save_json_to_file(json_dict, path)


def update_prices(urls_with_files, urls_with_prices_and_availability):
    for url in urls_with_prices_and_availability:
        new_price = urls_with_prices_and_availability[url][0]
        is_avilable = urls_with_prices_and_availability[url][1]
        update_the_price_and_availability(urls_with_files[url], url, new_price, is_avilable)


def update_availability(path, url, available):
    raise NotImplementedError()


