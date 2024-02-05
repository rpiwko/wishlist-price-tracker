"""
Module to find prices on taniaksiazka.pl
"""


import logging
from .base_dynamic_page_shop import base_dynamic_page_shop


class taniaksiazka(base_dynamic_page_shop):

    def get_element_to_wait(self):
        return "//p[@id='p-ourprice' and not(@style)]"


    def get_supported_domain(self):
        return "taniaksiazka.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_zl = html.find(id="updateable_price-zl")
            price_gr = html.find(id="updateable_price-gr")
            assert price_zl is not None and price_gr is not None, f"One or both price tags are None"
            price_string = price_zl.text + '.' + price_gr.text
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        availability_info = html.find(id="tmp-unavaialb")
        if availability_info:
            assert availability_info.text in ["Chwilowo niedostępny", "Produkt niedostępny"],\
                f"Unexpected availability info found: {availability_info.text}"
            return False
        preorder_info = html.find("div", class_="product-info").find_all("a", href="/Zapowiedzi")
        if len(preorder_info) > 0:
            logging.info("This offer is preorder!")
            return False
        return True
