"""
Module to find prices on mystic.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class mystic(base_static_page_shop):

    def get_supported_domain(self):
        return "mystic.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # The is_available is False for:
            # 1. Preorder: the price is shown
            # 2. Retired: price is hidden
            price_tag = html.find_all("strong", class_="projector_price_value")
            if is_available:
                assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            if len(price_tag) > 0:
                price_string = price_tag[0].text
                logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        warn_panel = html.find("div", class_="menu_messages_warning_sub")
        if warn_panel and "Szukany produkt nie został znaleziony" in warn_panel.text.strip():
            return False
        preorder_info = html.find("div", class_="product_pre_order")
        if preorder_info:
            return False
        return True
