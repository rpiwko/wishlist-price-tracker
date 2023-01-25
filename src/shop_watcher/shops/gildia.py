"""
Module to find prices on gildia.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class gildia(base_static_page_shop):

    def get_supported_domain(self):
        return "gildia.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # The is_available is False for:
            # 1. Preorder: the price is shown
            # 2. Retired: price is hidden
            price_tag = html.find_all("span", class_="current-price")
            if is_available:
                assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            if len(price_tag) > 0:
                price_string = price_tag[0].text
                logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        product_info_panels = html.find_all("div", class_="product-page-description")
        for product_info_panel in product_info_panels:
            prod_not_available_info = product_info_panel.find("a", class_="message-on-product-av")
            if prod_not_available_info and prod_not_available_info.text.strip() == \
                    "Kliknij tutaj, jeśli chcesz otrzymać maila, gdy produkt się ukaże.":
                return False
        return True
