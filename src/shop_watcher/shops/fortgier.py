"""
Module to find prices on fortgier.pl
"""


import logging
from .base_dynamic_page_shop import base_dynamic_page_shop


class fortgier(base_dynamic_page_shop):

    def get_element_to_wait(self):
        return "//div[@class='inventory-container']"


    def get_supported_domain(self):
        return "fortgier.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            price_panel = html.find_all("div", class_="pinfo-price price_produsts_info")
            assert len(price_panel) > 0, f"Price panel was not found"
            price_tag = price_panel[0].find_all("span", attrs={"itemprop": "price"})
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].get_text()
        return price_string, is_available


    def _is_available(self, html):
        # TODO: Update this method when find offer which is present in shop but not available to buy
        return True
