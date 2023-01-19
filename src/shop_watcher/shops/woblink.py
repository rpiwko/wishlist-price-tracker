"""
Module to find prices on woblink.com
"""


import logging
from .base_static_page_shop import base_static_page_shop


class woblink(base_static_page_shop):

    def get_supported_domain(self):
        return "woblink.com"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_availabe = None
        if html:
            is_available = self._is_available(html)
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not avilable
            price_panel = html.find_all("form", id="product-card-form")
            assert len(price_panel) == 1, f"Expected one price panel but getting {len(price_panel)}"
            price_sub_panels = price_panel[0].find_all("span", "cena price")
            assert len(price_panel) > 0, f"Unable to find price_sub_panels"
            if len(price_sub_panels) == 1:
                # Regular price
                price_tag = price_panel[0].find("span", class_="js-price")
            if len(price_sub_panels) > 1:
                # Discount
                price_tag = price_panel[0].find("span", class_="value promo-price").find("span", class_="js-price")
            price_string = price_tag.get_text()
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        unavailable_info = html.find_all("p", class_="stock-info__status")
        if len(unavailable_info) > 0 and unavailable_info[0].text.strip() == "Produkt niedostępny":
            return False
        else:
            return True
