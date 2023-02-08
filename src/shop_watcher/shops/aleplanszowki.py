"""
Module to find prices on aleplanszowki.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class aleplanszowki(base_static_page_shop):

    def get_supported_domain(self):
        return "aleplanszowki.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag = html.find_all("span", id="our_price_display")
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].text
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        product_status_tag = html.find_all("div", id="availability_statut")
        assert len(product_status_tag) == 1, f"Expected one item status tag but getting {len(product_status_tag)}"
        inner_prod_status_tag = product_status_tag[0].find_all("span", id="availability_value")
        assert len(inner_prod_status_tag) == 1, f"Expected one item status tag but getting {len(inner_prod_status_tag)}"
        if inner_prod_status_tag[0].text == "Ten produkt nie jest już dostępny":
            return False
        else:
            return True
