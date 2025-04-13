"""
Module to find prices on xjoy.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class xjoy(base_static_page_shop):

    def get_supported_domain(self):
        return "xjoy.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            box_info_product = html.find_all("div", class_="box-info-product")
            assert len(box_info_product) == 1, f"Expected one info product box but getting {len(box_info_product)}"
            price_tag = box_info_product[0].find_all("span", id="our_price_display")
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].get_text()
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        availability_value = html.find_all("span", id = "availability_value")
        assert len(availability_value) == 1, f"Expected one availability value but getting {len(availability_value)}"
        not_available = availability_value[0].get_text() == "Ten produkt nie występuje już w magazynie"
        if not_available:
            return False
        else:
            return True
