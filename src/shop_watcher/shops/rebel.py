"""
Module to find prices on rebel.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class rebel(base_static_page_shop):

    def get_supported_domain(self):
        return "rebel.pl"

    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag = html.find_all("span", attrs={"itemprop": "price"})
            if is_available or len(price_tag) == 1:
                assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
                price_string = price_tag[0].get("content")
                logging.info("price_string=" + price_string)
            else:
                # Product is not available and its page was removed too
                assert len(price_tag) == 0, f"Expected no tag but getting {len(price_tag)}"
        return price_string, is_available

    def _is_available(self, html):
        price_panel = html.find_all("div", class_="cart--quantity")
        assert len(price_panel) <= 1, f"Expected one or no item status tag but getting {len(price_panel)}"
        if len(price_panel) == 1:
            add_to_cart_btn = price_panel[0].find_all("button", class_="add-to-cart__btn")
            assert len(add_to_cart_btn) <= 1, f"Expected one or no item status tag but getting {len(add_to_cart_btn)}"
            if len(add_to_cart_btn) == 1:
                assert add_to_cart_btn[0].find("span").text.strip() == "Dodaj do koszyka", \
                    f"Unexpected button text: {add_to_cart_btn[0].text.strip()}"
                return True
        return False
