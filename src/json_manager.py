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
                

def update_the_price(path, url, new_price):
    json_dict = read_json_from_file(path)
    ts = datetime.now().strftime(time_format)
    logging.info("Updating price in file: " + str(path))
    logging.info("...for URL: " + str(url))
    logging.info("...with value: " + str(new_price))
    logging.info("...and TS: " + ts)
    for offer in json_dict["offers"]:
        if offer["url"] == url:
            logging.info("Old latestPrice: " + str(offer["latestPrice"]))
            logging.info("Old latestPriceDate: " + str(offer["latestPriceDate"]))
            offer["latestPrice"] = new_price
            offer["latestPriceDate"] = ts
            if new_price:
                if not offer["lowestPrice"] or offer["lowestPrice"] > new_price:
                    logging.info("Old lowestPrice: " + str(offer["lowestPrice"]))
                    logging.info("Old lowestPriceDate: " + str(offer["lowestPriceDate"]))
                    offer["lowestPrice"] = new_price
                    offer["lowestPriceDate"] = ts
            save_json_to_file(json_dict, path)


def update_prices(urls_with_files, urls_with_prices):
    for url in urls_with_prices:
        update_the_price(urls_with_files[url], url, urls_with_prices[url])


def update_availability(path, url, available):
    raise NotImplementedError()


