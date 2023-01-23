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
        is_availabe = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # If not is_available, then price is not shown so skip further checking
            if is_available:
                price_tag = html.find_all("span", class_="current-price")
                assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
                price_string = price_tag[0].text
                logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        product_info_panels = html.find_all("div", class_="product-page-description")
        for product_info_panel in product_info_panels:
            availability_info = product_info_panel.find("p", class_="light-font")
            if availability_info and availability_info.text == "Produkt jest aktualnie niedostępny":
                return False
        return True
