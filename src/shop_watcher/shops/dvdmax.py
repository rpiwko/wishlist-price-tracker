"""
Module to find prices on dvdmax.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class dvdmax(base_static_page_shop):

    def get_supported_domain(self):
        return "dvdmax.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # If not is_available, then price is not shown so skip further checking
            if is_available:
                price_tag_main = html.find_all("div", class_="price")
                assert len(price_tag_main) == 1, f"Expected one price tag but getting {len(price_tag_main)}"
                price_zl = price_tag_main[0].text
                price_tag_gr = price_tag_main[0].find_all("sup")
                assert len(price_tag_gr) == 1, f"Expected one price tag but getting {len(price_tag_gr)}"
                price_gr = price_tag_gr[0].text
                # Build the price string
                # e.g. for price_tag_main: <div class="price">49<sup>57</sup></div>
                # the price_zl = 4957
                pos_gr = price_zl.rfind(price_gr)
                price_zl = price_zl[:pos_gr]
                price_string = price_zl + "." + price_gr
                logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        product_status_tag = html.find_all("div", class_="unavailable")
        assert len(product_status_tag) <= 1, f"Expected max one item status tag but getting {len(product_status_tag)}"
        if len(product_status_tag) == 1:
            if product_status_tag[0].text == "Artykuł niedostępny":
                return False
            else:
                raise ValueError(f"Unexpected availability status: {product_status_tag[0].text}")
        else:
            return True
