"""
Module to find prices on lostintime.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class lostintime(base_static_page_shop):

    def get_supported_domain(self):
        return "lostintime.pl"

    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            offer_panel = html.find_all("div", class_="entry-summary")
            assert len(offer_panel) == 1, f"Expected one offer panel but getting {len(offer_panel)}"
            is_available = self._is_available(offer_panel[0])
            price_tag = offer_panel[0].find("ins").find_all("span", class_="woocommerce-Price-amount")
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].text
            logging.info("price_string=" + price_string)
        return price_string, is_available

    def _is_available(self, html):
        return len(html.find_all("p", class_="in-stock")) > 0
