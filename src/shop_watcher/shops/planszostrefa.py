"""
Module to find prices on planszostrefa.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class planszostrefa(base_static_page_shop):

    def get_supported_domain(self):
        return "planszostrefa.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag = html.find_all("em", class_="main-price")
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].text
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        prod_avail_panel = html.select("div.row.availability")
        assert len(prod_avail_panel) == 2, f"Expected two availability tags but getting {len(prod_avail_panel)}"
        if prod_avail_panel[1].find("span", class_="second").text == "niedostępny":
            return False
        else:
            add_to_basket_btn = html.find("button", class_="addtobasket")
            if add_to_basket_btn:
                return True
        raise ValueError("Unable to determine item availability")
