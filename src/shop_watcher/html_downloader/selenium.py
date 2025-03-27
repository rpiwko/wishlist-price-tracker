"""
HTML downloader for dynamic pages
"""


import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import math
from .. import string_tools


# WebDriver instances for different domains
drivers = {}

# Delays range used to avoid being banned
delay_min_sec = 2
delay_max_sec = 6

# How long WebDriver will poll DOM for element_to_wait or DOM to be stable
implicit_wait_in_seconds = 30


def get_the_html(url, element_to_wait=None, quit_webdriver=True):
    """
    Downloads HTML from URL

    Args:
        url (str): web page address to get the HTML from
        element_to_wait (str): xpath pointing page element for which WebDriver will wait before reading the HTML;
            if it's not defined (None), then page readiness will be determined base on DOM stability. This is slow
            and thus not recommended approach. Use only if other methods fail (e.g. for pages with price
            or availability being updated by background JS without other visible impact)
        quit_webdriver (bool): if True, then driver.quit() will be called in finally block 

    Returns:
        BeautifulSoup object created with "html.parser" and representing HTML page
    """

    domain = string_tools.get_domain_from_url(url)
    logging.info(f"[{domain}] Getting HTML with html_downloader.selenium for URL={url}")

    global drivers

    def _quit_webdriver():
        drivers[domain].quit()
        del drivers[domain]
        logging.info(f"[{domain}] WebDriver object was disposed. Remained WebDrivers: {str(drivers)}")

    try:
        _create_driver_if_needed(domain)
        drivers[domain].get(url)
        if element_to_wait:
            drivers[domain].find_element(By.XPATH, element_to_wait)
        else:
            try:
                _wait_until_dom_is_stable(domain)
            except TimeoutError:
                logging.warning(f"[{domain}] Timeout! Price and availability will be determined using unstable DOM. "
                              f"URL={url}")
        raw_html_string = drivers[domain].page_source
        return BeautifulSoup(raw_html_string, "html.parser")
    except Exception as e:
        logging.error(f"[{domain}] Unhandled exception occurred: {str(e)}")
        quit_webdriver = True
        # TODO: Add mechanism to automatic retry
        raise
    finally:
        if quit_webdriver:
            _quit_webdriver()


def get_htmls(url_list, element_to_wait=None):
    urls_with_htmls = {}
    for url in url_list:
        domain = string_tools.get_domain_from_url(url)
        try:
            if url_list.index(url) < len(url_list) - 1:
                urls_with_htmls[url] = get_the_html(url, element_to_wait=element_to_wait, quit_webdriver=False)
                _pause_execution(domain)
            else:
                urls_with_htmls[url] = get_the_html(url, element_to_wait=element_to_wait)
        except Exception as e:
            logging.error(f"[{domain}] Unable to extract HTML from URL={url} because of error: {str(e)}")
            urls_with_htmls[url] = None
            if url_list.index(url) < len(url_list) - 1:
                _pause_execution(domain, 60)
            continue

    return urls_with_htmls


def _create_driver_if_needed(domain):
    global drivers
    logging.info(f"[{domain}] Available WebDrivers: {str(drivers)}")
    if domain not in drivers.keys():
        logging.info(f"[{domain}] WebDriver not found. New instance will be created")
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        drivers[domain] = webdriver.Firefox(
            # TODO: Parametrize the log path
            service=Service("/usr/local/bin/geckodriver", log_path="geckodriver.log"),
            options=firefox_options)
        drivers[domain].implicitly_wait(implicit_wait_in_seconds)
    else:
        logging.info(f"[{domain}] WebDriver found. No need to create new one")


def _pause_execution(domain, pause_time_in_sec=0):
    if pause_time_in_sec:
        logging.info(f"[{domain}] Pausing execution for {pause_time_in_sec}s")
        time.sleep(pause_time_in_sec)
    else:
        pause_time_in_sec = random.randint(delay_min_sec, delay_max_sec)
        logging.info(f"[{domain}] Pausing execution for {pause_time_in_sec}s")
        time.sleep(pause_time_in_sec)


def _wait_until_dom_is_stable(domain):
    check_interval = 5
    for i in range(0, math.ceil(implicit_wait_in_seconds/check_interval)):
        prev_state = drivers[domain].page_source
        time.sleep(check_interval)
        if prev_state == drivers[domain].page_source:
            logging.info(f"[{domain}] DOM is stable after {i*check_interval + check_interval} seconds ")
            return
        logging.info(f"[{domain}] DOM is not stable. Still waiting...")
    raise TimeoutError(f"Unable to get stable DOM after defined amount of time ({implicit_wait_in_seconds}s)!")
