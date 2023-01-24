"""
HTML downloader for static pages
"""


import logging
from requests import get, RequestException
from bs4 import BeautifulSoup
import time
import random


# Delays range used to avoid being banned
delay_min_sec = 2
delay_max_sec = 6


def get_the_html(url, ignore_response_codes=[]):
    # TODO: Consider removing ignore_response_codes parameter
    """
    Downloads HTML from URL

    Args:
        url (str): web page address to get the HTML from
        ignore_response_codes (list): response codes which won't throw exception

    Returns:
        BeautifulSoup object created with "html.parser" and representing HTML page
    """
    logging.info("Getting HTML with html_downloader.requests for URL=" + url)
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'}
        r = get(url, timeout=60, headers=headers)
        if _is_good_response(r, ignore_response_codes):
            raw_html_string = r.text
            logging.debug(f"Downloaded HTML:\n{raw_html_string}")
            return BeautifulSoup(raw_html_string, "html.parser")
        else:
            error_text = "Request failed or response does not contain valid HTML!\n"
            error_text += f"Returned status code: {r.status_code}\n"
            error_text += f"Returned content type: {r.headers['Content-Type']}\n"
            # error_text += f"Returned text: {r.text}\n"
            logging.error(error_text)
            # TODO: Consider creating custom exception to handle different scenarios
            r.raise_for_status()
            raise ValueError("Response does not contain valid HTML!")
    except RequestException as e:
        logging.error(f"Unhandled exception occurred!\n{str(e)}")
        # TODO: Add mechanism to automatic retry
        raise


def get_htmls(url_list):
    urls_with_htmls = {}
    for url in url_list:
        try:
            urls_with_htmls[url] = get_the_html(url)
            if url_list.index(url) < len(url_list) - 1:
                _pause_execution()
        except Exception as e:
            logging.error(f"Unable to extract HTML from URL='{url}' because of error:\n{str(e)}")
            urls_with_htmls[url] = None
            continue
    return urls_with_htmls


def _is_good_response(resp, ignore_response_codes):
    """
    Validates the response

    Args:
        resp (Response): response to check
        ignore_response_codes (list): list of response codes for which True is always returned

    Returns:
        True when response code 200 and content type is HTML
        True when response code different than 200 but on ignore_response_codes list
        False otherwise
    """
    logging.debug("START: download_component._is_good_response()")
    logging.debug(f"resp={resp}")

    content_type = resp.headers['Content-Type'].lower()

    if resp.status_code in ignore_response_codes:
        logging.warning(f"Received '{resp.status_code}' response code, but it's on ignore list. Further validation skipped.")
        return True
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def _pause_execution(pause_time_in_sec=0):
    if pause_time_in_sec:
        logging.info(f"Pausing execution for {pause_time_in_sec}s")
        time.sleep(pause_time_in_sec)
    else:
        pause_time_in_sec = random.randint(delay_min_sec, delay_max_sec)
        logging.info(f"Pausing execution for {pause_time_in_sec}s")
        time.sleep(pause_time_in_sec)
