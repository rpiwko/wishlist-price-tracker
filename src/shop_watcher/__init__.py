"""
Expose main module methods which extract prices from passed URLs
"""


from .get_the_price import get_the_price
from .get_prices import get_prices

# Importing shop modules
import os
import importlib
for file in os.listdir(os.path.dirname(__file__) + "/shops/"):
    if file.endswith(".py") and file != "base_shop.py":
        module_name = "shop_watcher.shops." + file[:-3]
        # print("Loading module: " + module_name)
        globals()[module_name] = importlib.import_module(module_name)
