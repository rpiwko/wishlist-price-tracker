"""
Module to gather download functionalities for static pages. 
Handles requests and responses.
"""


import logging
from requests import get, RequestException
from bs4 import BeautifulSoup
# from requests.exceptions import
from contextlib import closing


def get_the_html(url, return_bs4_object = False, ignore_response_codes=[]):
    """
    Downloads HTML from URL

    Args:
        url (str): web page address to get the HTML from
        ignore_response_codes (list): response codes which won't throw exception
        return_bs4_object (bool): flag to return pure string or BeautifulSoup object

    Returns:
        If return_bs4_object is False then then HTML string downloaded from URL
        If return_bs4_object is True then BeautifulSoup object created with "html.parser"
    """
    logging.info("START: download_component.get_the_html()")
    logging.info(f"URL={url}")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'}
        r = get(url, timeout=60, headers=headers)
        if _is_good_response(r, ignore_response_codes):
            raw_html_string = r.text
            logging.debug(f"Downloaded HTML:\n{raw_html_string}")
            if return_bs4_object:
                return  BeautifulSoup(raw_html_string, "html.parser")
            else:
                return raw_html_string
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
        raise
    finally:
        logging.info("END: download_component.get_the_html()")
    

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
