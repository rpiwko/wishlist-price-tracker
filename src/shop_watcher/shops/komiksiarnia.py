"""
Module to find prices on komiksiarnia.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class komiksiarnia(base_static_page_shop):

    def get_supported_domain(self):
        return "komiksiarnia.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag = html.find_all("div", class_="current-price")
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].find("span", attrs={"itemprop": "price"}).text
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        product_availability_panel = html.find("span", id="product-availability")
        if product_availability_panel.find("i", class_="product-available") and \
                "W magazynie" in product_availability_panel.text.strip():
            return True
        if product_availability_panel.find("i", class_="product-unavailable") and \
                "Obecnie brak na stanie" in product_availability_panel.text.strip():
            return False
        raise ValueError("Unable to determine item availability")
