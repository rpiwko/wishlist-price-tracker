"""
Module to find prices on ebookpoint.pl
"""


import logging
from .base_dynamic_page_shop import base_dynamic_page_shop


class ebookpoint(base_dynamic_page_shop):

    def get_element_to_wait(self):
        return None

    def get_supported_domain(self):
        return "ebookpoint.pl"

    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag = html.find_all(id="cena_e")
            assert len(price_tag) == 1, f"Expected one tag with id='cena_e' but getting {len(price_tag)}"
            price_string = price_tag[0].get_text()
            logging.info("price_string=" + price_string)
        return price_string, is_available

    def _is_available(self, html):
        not_available_tag = html.find_all(class_="tag-navailable")
        return (len(not_available_tag) == 0 or
                (len(not_available_tag) > 0 and not_available_tag[0].get("style") == "display:none;"))
