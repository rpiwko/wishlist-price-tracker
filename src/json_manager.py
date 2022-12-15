"""
Module to manage json files with wishlist items
"""


import logging
import json


def read_json_from_file(path):
    with open(path, "r") as json_file:
        data = json.load(json_file)
    print(data)        
    return data


def save_json_to_file(json_string, path):
    with open(path, "w") as json_file:
        json.dump(json_string, json_file, indent=4)
