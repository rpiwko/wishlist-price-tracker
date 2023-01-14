"""
Module to find prices on planszomania.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class planszomania(base_static_page_shop):

    def get_supported_domain(self):
        return "planszomania.pl"


    def _find_price_in_html(self, html):
        if html:
            price_tag = html.find_all("div", id="price_tag")
            assert len(price_tag) == 1, f"Expected one <price_tag> tag but getting {len(price_tag)}"
            price_string = price_tag[0].find("strong").get_text()
            return price_string
