"""
Module to find prices on mangastore.pl
"""


import logging
from .base_static_page_shop import base_static_page_shop


class mangastore(base_static_page_shop):

    def get_supported_domain(self):
        return "mangastore.pl"


    def _get_price_and_availability_from_html(self, html):
        price_string = None
        is_available = None
        if html:
            offer_panel = html.find_all("div", id="KupowanieProduktu")
            assert len(offer_panel) == 1, f"Expected one offer details panel but getting {len(offer_panel)}"
            is_available = self._is_available(offer_panel[0])
            logging.info("is_available=" + str(is_available))
            # Price is still shown even when item is not available
            price_tag = offer_panel[0].find_all("p", id="CenaGlownaProduktuBrutto")
            assert len(price_tag) == 1, f"Expected one price tag but getting {len(price_tag)}"
            price_string = price_tag[0].text
            logging.info("price_string=" + price_string)
        return price_string, is_available


    def _is_available(self, html):
        availability_panel = html.find_all("p", id="InfoNiedostepny")
        assert len(availability_panel) == 1, f"Expected one availability panel but getting {len(availability_panel)}"
        try:
            if availability_panel[0]["style"] == "display:none":
                # Check if preorder
                preorder_info = html.find_all("p", id="DataDostepnosci")
                if len(preorder_info) > 0 and "PREORDER" in preorder_info[0].text.upper():
                    logging.info("This offer is preorder!")
                    return False
                return True
        except KeyError:
            return False
        except Exception as e:
            raise ValueError(f"Unable to determine item availability because of exception:\n{str(e)}")
        raise ValueError("Unable to determine item availability")
