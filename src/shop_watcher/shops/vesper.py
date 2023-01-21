"""
Module to find prices on vesper.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class vesper(base_static_page_shop):

    def get_supported_domain(self):
        return "vesper.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag = html.find_all("span", id="our_price_display", attrs={"class": "price", "itemprop": "price"})
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].get_text()
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        add_to_cart_btn = html.find("p", id="add_to_cart")
        before_release_info = html.find("div", id="short_description_block")
        before_release_info_text = ""
        if before_release_info:
            before_release_info_text = before_release_info.find(lambda tag:tag.name=="span" and "Premiera:" in tag.text)
        if before_release_info_text or not add_to_cart_btn:
            return False
        if add_to_cart_btn:
            return True
        raise ValueError("Unable to determine item availability")
