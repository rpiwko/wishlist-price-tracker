"""
Module to find prices on nexto.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class nexto(base_static_page_shop):

    def get_supported_domain(self):
        return "nexto.pl"


    def _find_price_in_html(self, html):
        if html:
            price_tag = html.find_all("div", class_="prices")
            assert len(price_tag) == 1, f"Expected one <prices> tag but getting {len(price_tag)}"
            price_string = price_tag[0].find("strong", class_="price").get_text()
            logging.info("price_string=" + price_string)
            return price_string
