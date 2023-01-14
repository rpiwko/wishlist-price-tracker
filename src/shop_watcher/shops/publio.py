"""
Module to find prices on publio.pl
"""


import logging
from .base_dynamic_page_shop import base_dynamic_page_shop


class publio(base_dynamic_page_shop):

    def get_element_to_wait(self):
        return "//div[@class='prices']"


    def get_supported_domain(self):
        return "publio.pl"


    def _find_price_in_html(self, html):
        if html:
            price_tag = html.find_all("div", class_="prices")
            assert len(price_tag) == 1, f"Expected one <prices> tag but getting {len(price_tag)}"
            price_string = price_tag[0].find("div", class_="current").get_text()
            return price_string
