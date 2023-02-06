"""
Module to find prices on swiatksiazki.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class swiatksiazki(base_static_page_shop):

    def get_supported_domain(self):
        return "swiatksiazki.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag_main = html.find_all("div", class_="product-info-price")
            assert len(price_tag_main) == 1, f"Expected one price tag but getting {len(price_tag_main)}"
            price_tag_inner = price_tag_main[0].find("span", class_="price")
            assert len(price_tag_inner) == 1, f"Expected one price tag but getting {len(price_tag_inner)}"
            price_string = price_tag_inner.text
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        # TODO: Update this method when find offer which is present in shop but not available to buy
        return True
