"""
Module to find prices on mepel.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class mepel(base_static_page_shop):

    def get_supported_domain(self):
        return "mepel.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            offer_panel = html.find_all("div", class_="bottomborder")
            assert len(offer_panel) == 1, f"Expected one offer details panel but getting {len(offer_panel)}"
            is_available = self._is_available(offer_panel[0])
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag = offer_panel[0].find_all("em", class_="main-price")
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].text
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        availability_panel = html.find_all("div", class_ = "availability")
        assert len(availability_panel) == 1, f"Expected one availability panel but getting {len(availability_panel)}"
        available_icon = availability_panel[0].find("span", class_="green")
        not_available_icon = availability_panel[0].find("span", class_="gray")
        preorder_icon = availability_panel[0].find("span", class_="red")
        if available_icon and available_icon.find("em").text.strip() == "dostępna":
            return True
        if not_available_icon and not_available_icon.find("em").text.strip() == "brak towaru":
            return False
        if preorder_icon and preorder_icon.find("em").text.strip() == "przedsprzedaż":
            return False
        raise ValueError("Unable to determine item availability")
