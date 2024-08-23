"""
Module to find prices on ebookpoint.pl
"""


import logging
from .base_dynamic_page_shop import base_dynamic_page_shop


class ebookpoint(base_dynamic_page_shop):

    def get_element_to_wait(self):
        return None

    def get_supported_domain(self):
        return "ebookpoint.pl"

    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            if self._page_exists(html):
                # Price is still shown even when item is not available
                price_tag = html.find_all(id="cena_e")
                assert len(price_tag) == 1, f"Expected one tag with id='cena_e' but getting {len(price_tag)}"
                price_string = price_tag[0].get_text()
                logging.info("price_string=" + price_string)
            else:
                logging.info("Product page was removed!")
        return price_string, is_available

    def _is_available(self, html):
        if not self._page_exists(html):
            # Product is not available and its page was removed too
            return False
        not_available_tag = html.find_all(class_="tag-navailable")
        if len(not_available_tag) == 0:
            # Product is available
            return True
        if len(not_available_tag) > 0 and not_available_tag[0].get("style") == "display:none;":
            # Product is available but other format is not
            return True
        else:
            # Product is not available but its page is still there
            return False

    def _page_exists(self, html):
        book_details_section = html.find_all(class_='book-details')
        assert len(book_details_section) <= 1, f"Expected max one book details section but getting {len(book_details_section)}"
        return len(book_details_section) == 1
