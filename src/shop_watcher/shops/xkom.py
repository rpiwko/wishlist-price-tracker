"""
Module to find prices on x-kom.pl
"""


import logging
from .base_dynamic_page_shop import base_dynamic_page_shop
from shop_watcher import string_tools
import fnmatch


class xkom(base_dynamic_page_shop):

    def get_element_to_wait(self):
        return "/html/body/div[1]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[1]"

    def get_supported_domain(self):
        return "x-kom.pl"

    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            if is_available:
                divs = html.find_all("div")
                assert len(divs) > 300, f"Expected more than 300 <div> tags but getting {len(divs)}"
                for i in range(300, 400):
                    price_string_candidate = divs[i].text
                    if price_string_candidate and "zł" in price_string_candidate:
                        try:
                            string_tools.format_and_validate_the_price(price_string_candidate)
                            logging.info(f"Price='{price_string_candidate}' found on index={i}")
                            price_string = price_string_candidate
                            break
                        except ValueError:
                            continue
                logging.info("price_string=" + price_string_candidate)
        return price_string, is_available

    def _is_available(self, html):
        pattern = "*Czasowo niedostępny*"
        return not fnmatch.fnmatch(str(html), pattern)
