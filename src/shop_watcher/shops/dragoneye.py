"""
Module to find prices on dragoneye.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class dragoneye(base_static_page_shop):

    def get_supported_domain(self):
        return "dragoneye.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_container = html.find_all("div", id="szczegolyProduktu")
            assert len(price_container) == 1, f"Expected one price tag but getting {len(price_container)}"
            price_tag_inner = price_container[0].find("span", class_="cenaBrutto")
            assert len(price_tag_inner) == 1, f"Expected one price tag but getting {len(price_tag_inner)}"
            price_string = price_tag_inner.text
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        add_to_basket_btn = html.find_all("input", attrs = {"class": "button", "type": "submit", "value": "Do koszyka"})
        assert len(add_to_basket_btn) <= 1, f"Expected max one submit button but getting {len(add_to_basket_btn)}"
        if len(add_to_basket_btn) == 1:
            return True
        else:
            return False
