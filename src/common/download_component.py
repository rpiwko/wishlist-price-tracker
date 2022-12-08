"""
Module to gather download functionalities. 
Handles requests and responses.
"""


import logging
from requests import get, RequestException
# from requests.exceptions import
from contextlib import closing


def get_the_html(url, ignore_response_codes=[]):
    """
    Downloads HTML from URL

    Args:
        url (str): web page address to get the HTML from
        ignore_response_codes (list): response codes which won't throw exception

    Returns:
        The HTML downloaded from URL, otherwise None
    """
    logging.info("START: download_component.get_the_html()")
    logging.info("URL={0}".format(url))
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'}
        r = get(url, timeout=60, headers=headers)
        if _is_good_response(r, ignore_response_codes):
            logging.debug("Downloaded HTML:\n{0}".format(r.text))
            return r.text
        else:
            error_text = "Request failed or response does not contain valid HTML!\n"
            error_text += "Returned status code: {0}\n".format(r.status_code)
            error_text += "Returned content type: {0}\n".format(r.headers['Content-Type'])
            # error_text += "Returned text: {0}\n".format(r.text)
            logging.error(error_text)
            # TODO: Consider creating custom exception to handle different scenarios
            r.raise_for_status()
            raise ValueError("Response does not contain valid HTML!")
    except RequestException as e:
        logging.error("Unhandled exception occurred!\n{0}".format(str(e)))
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
        True when response code in ignore_response_codes
        False otherwise
    """
    logging.debug("START: download_component._is_good_response()")
    logging.debug("resp={0}".format(resp))

    content_type = resp.headers['Content-Type'].lower()

    if resp.status_code in ignore_response_codes:
        logging.warning("Received '{}' response code, but it's on ignore list. Further validation skipped.".
                        format(resp.status_code))
        return True
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)
