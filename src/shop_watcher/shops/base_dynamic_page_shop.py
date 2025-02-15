"""
Base class for shops with dynamic pages
"""


import logging
from ..html_downloader import selenium as html_downloader


class base_dynamic_page_shop:

    def get_element_to_wait(self):
        """
        Returns xpath pointing page element for which html_downloader will wait before getting the HTML.
        If None returned, then page readiness will be determined base on DOM stability. This is slow and thus
        not recommended approach. Use only if other methods fail (e.g. for pages with price or availability
        being updated by background JS without other visible impact)
        """
        raise NotImplementedError("The get_element_to_wait() method needs to be \
overridden in each class which inherits from base_dynamic_page_shop!")

    def get_supported_domain(self):
        raise NotImplementedError("The get_supported_domain() method needs to be \
overridden in each class which inherits from base_dynamic_page_shop!")

    def get_the_price(self, url):
        """
        Gets the price from single URL. The _find_price_in_html() method needs to be overridden 
        in each class which inherits from base_dynamic_page_shop

        Args:
            url(str): URL to web store item

        Returns:
            Tuple with raw price text extracted from HTML and availability flag
        """
        return self._get_price_and_availability_from_html(html_downloader.get_the_html(url, element_to_wait=self.get_element_to_wait()))

    def get_prices(self, url_list):
        """
        Get the price from multiple URLs

        Args:
            url_list: list of URLs to get the prices from

        Returns:
            Dictionary with URLs, raw price texts and availability flags:
            {"url1": ("raw_price_text1", True), "url2": ("raw_price_text2", True), "url3": ("raw_price_text3", False)...}
        """
        urls_with_prices = {}
        urls_with_htmls = html_downloader.get_htmls(url_list, element_to_wait=self.get_element_to_wait())
        for url in urls_with_htmls:
            logging.info("Searching price and availability in HTML for URL=" + url)
            try:
                urls_with_prices[url] = self._get_price_and_availability_from_html(urls_with_htmls[url])
            except Exception as e:
                logging.error(f"Unable to extract price from HTML for URL='{url}' because of error: {str(e)}")
                urls_with_prices[url] = None
        return urls_with_prices

    def _get_price_and_availability_from_html(self, html):
        """
        Get the price from HTML. 
        This method needs to be overridden in each class which inherits from base_dynamic_page_shop

        Args:
            html (obj): BeautifulSoup object parsed with html.parser

        Returns:
            Tuple with raw price text extracted from HTML and availability flag
            None if html was None
        """
        raise NotImplementedError("The _get_price_and_availability_from_html() method needs to be \
overridden in each class which inherits from base_dynamic_page_shop!")
