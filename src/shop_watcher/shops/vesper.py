"""
Module to find prices on vesper.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class vesper(base_static_page_shop):

    def get_supported_domain(self):
        return "vesper.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            add_to_cart_field = html.find_all("div", class_="pole_dodawania_do_koszyka")
            assert len(add_to_cart_field) == 1, f"Expected one add to cart field but getting {len(add_to_cart_field)}"
            is_available = self._is_available(add_to_cart_field)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag = html.find_all("span", class_="current-price-value")
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].get("content")
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        not_available = len(html[0].find_all("i", call_ = "product-unavailable")) > 0
        if not_available:
            return False
        else:
            return True
