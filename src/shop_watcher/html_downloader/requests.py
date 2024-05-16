"""
HTML downloader for static pages
"""


import logging
import requests.exceptions
from requests import get, RequestException
from bs4 import BeautifulSoup
import time
import random
from .. import string_tools


# Delays range used to avoid being banned
delay_min_sec = 5
delay_max_sec = 10

# How many times retry download in case of error
max_retries = 3


def get_the_html(url):
    """
    Downloads HTML from URL

    Args:
        url (str): web page address to get the HTML from

    Returns:
        BeautifulSoup object created with "html.parser" and representing HTML page
        Empty string ("") when 404 was received
    """

    domain = string_tools.get_domain_from_url(url)
    logging.info(f"[{domain}] Getting HTML with html_downloader.requests for URL={url}")

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0"}
    attempt_no = 1

    while True:
        try:
            r = get(url, timeout=60, headers=headers)
            if r.status_code == 404:
                logging.warning(f"[{domain}] 404: page not found!")
                return ""
            if _is_response_ok(r):
                raw_html_string = r.text
                logging.debug(f"Downloaded HTML:\n{raw_html_string}")
                return BeautifulSoup(raw_html_string, "html.parser")
            else:
                error_text = f"response status code: {r.status_code}; response headers: {r.headers}"
                # error_text += f"\nReturned text: {r.text}"
                raise requests.exceptions.HTTPError(error_text)
        except RequestException as e:
            logging.error(f"[{domain}] Unable to get HTML for URL='{url}' Attempt: {attempt_no} of {max_retries}. "
                          f"Error details: {str(e)}")
            if attempt_no < max_retries:
                _pause_execution(domain, pause_time_in_sec=(attempt_no * 60))
                attempt_no += 1
                logging.info(f"[{domain}] Retrying... Attempt {attempt_no} of {max_retries}...")
            else:
                raise


def get_htmls(url_list):
    urls_with_htmls = {}
    for url in url_list:
        domain = string_tools.get_domain_from_url(url)
        try:
            urls_with_htmls[url] = get_the_html(url)
            if url_list.index(url) < len(url_list) - 1:
                _pause_execution(domain)
        except Exception as e:
            logging.error(f"[{domain}] Unable to get HTML for URL='{url}'. Check earlier logs for details.")
            urls_with_htmls[url] = None
            if url_list.index(url) < len(url_list) - 1:
                _pause_execution(domain, pause_time_in_sec=60)
            continue
    return urls_with_htmls


def _is_response_ok(resp):
    """
    Validates the response

    Args:
        resp (Response): response to check

    Returns:
        True when response code 200 and content type is HTML
        True when response code different than 200 but on ignore_response_codes list
        False otherwise
    """
    logging.debug("START: download_component._is_response_ok()")
    logging.debug(f"resp={resp}")

    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def _pause_execution(domain, pause_time_in_sec=0):
    if pause_time_in_sec:
        logging.info(f"[{domain}] Pausing execution for {pause_time_in_sec}s")
        time.sleep(pause_time_in_sec)
    else:
        pause_time_in_sec = random.randint(delay_min_sec, delay_max_sec)
        logging.info(f"[{domain}] Pausing execution for {pause_time_in_sec}s")
        time.sleep(pause_time_in_sec)
