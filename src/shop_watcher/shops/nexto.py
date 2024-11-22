"""
Module to find prices on nexto.pl
"""


import logging
import fnmatch
from .base_static_page_shop import base_static_page_shop


class nexto(base_static_page_shop):

    def get_supported_domain(self):
        return "nexto.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # If not is_available, then price is not shown so skip further checking
            if is_available:
                price_section = html.find_all("div", class_="buybox-in issue")
                assert len(price_section) == 1, f"Expected one price section but getting {len(price_section)}"

                premium_price = price_section[0].find_all("div", class_="option option-cart premium")
                assert len(premium_price) == 1, f"Expected one premium price but getting {len(premium_price)}"
                premium_price[0].decompose()

                price_tag = price_section[0].find_all("div", class_="prices")
                assert len(price_tag) == 1, f"Expected one <prices> tag but getting {len(price_tag)}"

                price_string = price_tag[0].find("strong", class_="price").get_text()
                logging.info("price_string=" + price_string)

        return price_string, is_available


    def _is_available(self, html):
        pattern = "*Przepraszamy, ale produkt „*” nie jest dostępny.*"
        return not fnmatch.fnmatch(str(html), pattern)
