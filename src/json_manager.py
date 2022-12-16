"""
Module to manage json files with wishlist items
"""


import logging
import json
from datetime import datetime
from pathlib import Path


time_format = "%Y-%m-%d %H:%M"


def read_json_from_file(path):
    with open(path, "r") as json_file:
        data = json.load(json_file)
    return data


def save_json_to_file(json_dict, path):
    with open(path, "w") as json_file:
        json.dump(json_dict, json_file, indent=4)


def get_offer_urls(path_to_file):
    json_dict = read_json_from_file(path_to_file)
    urls = []
    for offer in json_dict["offers"]:
        urls.append(offer["url"])
    return urls


def get_offers_urls(path_to_dir):
    urls_to_return = {}
    for json_file in sorted(Path(path_to_dir).glob("**/*.json")):
        urls_in_json = get_offer_urls(json_file)
        if urls_in_json:
            for url in urls_in_json:
                if url in urls_to_return:
                    error_text = "The same URL in two different json files is not supported:"
                    error_text += "\nURL: " + url
                    error_text += "\nFile1: " + str(urls_to_return[url])
                    error_text += "\nFile2: " + str(json_file)
                    raise KeyError(error_text)
                urls_to_return[url] = json_file
    return urls_to_return
                

def update_price(path, url, new_price):
    json_dict = read_json_from_file(path)
    for offer in json_dict["offers"]:
        if offer["url"] == url:
            ts = datetime.now().strftime(time_format)
            offer["latestPrice"] = new_price
            offer["latestPriceDate"] = ts
            if not offer["lowestPrice"] or  (offer["lowestPrice"] and offer["lowestPrice"] > new_price):
                offer["lowestPrice"] = new_price
                offer["lowestPriceDate"] = ts
            save_json_to_file(json_dict, path)


def update_availability(path, url, available):
    raise NotImplementedError()


