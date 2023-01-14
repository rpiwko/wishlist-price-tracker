"""
Module to find prices on virtualo.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class virtualo(base_static_page_shop):

    def get_supported_domain(self):
        return "virtualo.pl"


    def _find_price_in_html(self, html):
        if html:
            price_tag = html.find_all("div", class_="price-main")
            assert len(price_tag) == 1, f"Expected one <price-main> tag but getting {len(price_tag)}"
            price_string = price_tag[0].find("span", itemprop="price").get_text()
            return price_string
