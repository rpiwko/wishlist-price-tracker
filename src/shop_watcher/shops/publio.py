"""
Module to find prices on publio.pl
"""


import logging
from .base_dynamic_page_shop import base_dynamic_page_shop


class publio(base_dynamic_page_shop):

    def get_element_to_wait(self):
        return "//div[@class='price']"


    def get_supported_domain(self):
        return "publio.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # If not is_available, then price is not shown so skip further checking
            if is_available:
                price_tag = html.find_all("div", class_="prices")
                assert len(price_tag) == 1, f"Expected one <prices> tag but getting {len(price_tag)}"
                price_string = price_tag[0].find("div", class_="current").get_text()
        return price_string, is_available


    def _is_available(self, html):
        unavailable_info = html.find_all("div", class_="unavailable-info")
        if len(unavailable_info) > 0 and unavailable_info[0].text.strip() == "Produkt niedostępny":
            return False
        else:
            return True
