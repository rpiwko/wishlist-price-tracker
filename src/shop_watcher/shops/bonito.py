"""
Module to find prices on bonito.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class bonito(base_static_page_shop):

    def get_supported_domain(self):
        return "bonito.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag = html.find_all("div", attrs={"itemprop": "price"})
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].get_text()
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        availability_info_when_in_stock = html.find("span", attrs={"itemprop": "availability"})
        availability_info_when_out_of_stock = html.find("div", attrs={"itemprop": "availability"})
        if availability_info_when_in_stock and availability_info_when_in_stock.get("content") != "OutOfStock":
            return True
        if availability_info_when_out_of_stock and availability_info_when_out_of_stock.get("content") == "OutOfStock":
            return False
        raise ValueError("Unable to determine item availability")
