"""
Module to find prices on strefamarzen.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class strefamarzen(base_static_page_shop):

    def get_supported_domain(self):
        return "strefamarzen.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_container = html.find_all("strong", id="projector_price_value")
            assert len(price_container) == 1, f"Expected one price tag but getting {len(price_container)}"
            price_tag_inner = price_container[0].find("span")
            assert len(price_tag_inner) == 1, f"Expected one price tag but getting {len(price_tag_inner)}"
            price_string = price_tag_inner.text
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        product_status_tag = html.find_all("div", id="projector_status_description")
        assert len(product_status_tag) == 1, f"Expected one item status tag but getting {len(product_status_tag)}"
        if product_status_tag[0].text == "Produkt niedostępny":
            return False
        else:
            return True
