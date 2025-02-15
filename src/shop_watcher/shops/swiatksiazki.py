"""
Module to find prices on swiatksiazki.pl
"""


import logging
from .base_dynamic_page_shop import base_dynamic_page_shop


class swiatksiazki(base_dynamic_page_shop):

    def get_element_to_wait(self):
        return None

    def get_supported_domain(self):
        return "swiatksiazki.pl"

    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag_main = html.find_all("div", class_="ProductPage-RightSummarySticky")
            assert len(price_tag_main) == 1, f"Expected one price tag but getting {len(price_tag_main)}"
            price_tag_inner = price_tag_main[0].find("span", class_="ProductPrice-PriceValue")
            assert len(price_tag_inner) == 1, f"Expected one price tag but getting {len(price_tag_inner)}"
            price_string = price_tag_inner.text
            logging.info("price_string=" + price_string)
        return price_string, is_available

    def _is_available(self, html):
        additional_info_section = html.find_all("span", class_ = "AdditionalInformation-Title")
        info_cnt = len(additional_info_section)
        assert info_cnt > 0, f"Unable to find info tag"
        assert info_cnt <= 3, f"Unexpected number of info tags: {info_cnt}"
        if info_cnt == 1:
            if additional_info_section[0].text == "Produkt do pobrania":
                return True
            if additional_info_section[0].text == "Produkt niedostępny":
                return False
            raise ValueError(f"Unexpected info text: {additional_info_section[0].text}")
        if info_cnt == 3:
            return True
