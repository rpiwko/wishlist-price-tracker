"""
Module to manage json files with wishlist items
"""


import logging
import json


def read_json_from_file(path):
    with open(path, "r") as json_file:
        data = json.load(json_file)
    return data


def save_json_to_file(json_dict, path):
    with open(path, "w") as json_file:
        json.dump(json_dict, json_file, indent=4)


def get_offer_urls(path):
    json_dict = read_json_from_file(path)
    urls = []
    for offer in json_dict["offers"]:
        urls.append(offer["url"])
    return urls
