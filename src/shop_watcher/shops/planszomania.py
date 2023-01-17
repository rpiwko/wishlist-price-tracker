"""
Module to find prices on planszomania.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class planszomania(base_static_page_shop):

    def get_supported_domain(self):
        return "planszomania.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not avilable
            price_tag = html.find_all("div", id="price_tag")
            assert len(price_tag) == 1, f"Expected one <price_tag> tag but getting {len(price_tag)}"
            price_string = price_tag[0].find("strong").get_text()
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        not_available_tag = html.find_all(lambda tag:tag.name=="span" and "niedostępny" in tag.text, class_="span_error")
        return len(not_available_tag) == 0
