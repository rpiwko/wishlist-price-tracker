"""
Module to find prices on virtualo.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class virtualo(base_static_page_shop):

    def get_supported_domain(self):
        return "virtualo.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # If not is_available, then price is not shown so skip further checking
            if is_available:
                price_tag = html.find_all("div", class_="price-main")
                assert len(price_tag) == 1, f"Expected one <price-main> tag but getting {len(price_tag)}"
                price_string = price_tag[0].find("span", itemprop="price").get_text()
                logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        suggestion_wrapper = html.find_all("div", class_="suggestion-wrapper")
        if len(suggestion_wrapper) > 0 and suggestion_wrapper[0].find("span").text.strip() == "Produkt niedostępny.":
            return False
        not_available_info = html.find_all(lambda tag:tag.name=="div" and "Produkt chwilowo niedostępny" in tag.text,
                                           class_="column")
        if len(not_available_info) > 0:
            return False
        return True
