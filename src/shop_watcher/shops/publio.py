"""
Module to find prices on publio.pl
"""


import logging
from .base_dynamic_page_shop import base_dynamic_page_shop


class publio(base_dynamic_page_shop):

    def get_element_to_wait(self):
        return "//div[@class='wrapper product-card__buy']"

    def get_supported_domain(self):
        return "publio.pl"

    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            product_card = html.find_all("div", class_="product-card__header")
            assert len(product_card) == 1, f"Expected one product card section but getting {len(product_card)}"
            is_available = self._is_available(product_card[0])
            logging.info("is_available=" + str(is_available))
            # If not is_available, then price is not shown so skip further checking
            if is_available:
                price_tag = product_card[0].find_all("div", class_="current-price")
                assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
                price_string = price_tag[0].get_text()
        return price_string, is_available

    def _is_available(self, html):
        unavailable_info = html.find_all("div", class_="unavailable-info")
        if len(unavailable_info) > 0 and unavailable_info[0].text.strip() == "Produkt niedostępny":
            return False
        else:
            return True
