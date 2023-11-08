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
            price_tag = html.find_all("span", class_="current-price-display")
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].text
            logging.info("price_string=" + price_string)
        return price_string, is_available

    def _is_available(self, html):
        inform_when_available_btn = html.find_all("button", class_="js-mailalert-add")
        assert len(inform_when_available_btn) <= 1, \
            f"Expected one or no item status tag but getting {len(inform_when_available_btn)}"
        if len(inform_when_available_btn) == 1:
            assert inform_when_available_btn[0].text.strip() == "Powiadom o dostępności", \
                f"Unexpected button text: {inform_when_available_btn[0].text.strip()}"
            return False
        else:
            return True
