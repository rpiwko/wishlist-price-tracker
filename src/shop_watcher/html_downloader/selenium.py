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


# WebDriver instance
driver = None

# Delays range used to avoid being banned
delay_min_sec = 2
delay_max_sec = 6

# How long WebDriver will poll DOM for element_to_wait
implicit_wait_in_seconds = 10


def get_the_html(url, element_to_wait=None, quit_webdriver=True):
    """
    Downloads HTML from URL

    Args:
        url (str): web page address to get the HTML from
        element_to_wait (str): xpath pointing page element for which WebDriver will wait before reading the HTML
        quit_webdriver (bool): if True, then driver.quit() will be called in finally block 

    Returns:
        BeautifulSoup object created with "html.parser" and representing HTML page
    """
    logging.info("START: html_downloader.selenium.get_the_html()")
    logging.info(f"URL={url}")
    global driver
    try:
        _create_driver_if_needed()
        driver.get(url)
        if element_to_wait:
            driver.find_element(By.XPATH, element_to_wait)
        raw_html_string = driver.page_source
        return  BeautifulSoup(raw_html_string, "html.parser")
    except Exception as e:
        logging.error(f"Unhandled exception occurred!\n{str(e)}")
        # TODO: Add mechanism to automatic retry
        raise
    finally:
        if quit_webdriver:
            driver.quit()
            driver = None
            logging.info("WebDriver object was disposed")
        logging.info("END: html_downloader.selenium.get_the_html()")


def get_htmls(url_list, element_to_wait=None):
    urls_with_htmls = {}
    for url in url_list:
        try:
            if url_list.index(url) < len(url_list) - 1:
                urls_with_htmls[url] = get_the_html(url, element_to_wait=element_to_wait, quit_webdriver=False)
                _pause_execution()
            else:
                urls_with_htmls[url] = get_the_html(url, element_to_wait=element_to_wait)
        except Exception as e:
            logging.error(f"Unable to extract HTML from URL='{url}' because of error:\n{str(e)}")
            urls_with_htmls[url] = None
            continue

    return urls_with_htmls


def _create_driver_if_needed():
    global driver
    if not driver:
        logging.info("WebDriver not found. New instance will be created")
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(service=Service("/usr/local/bin/geckodriver", log_path="geckodriver.log"), # TODO: Parametrize the log path
                                options=firefox_options)
        driver.implicitly_wait(implicit_wait_in_seconds)
    else:
        logging.info("WebDriver found. No need to create new one")


def _pause_execution(pause_time_in_sec=0):
    if pause_time_in_sec:
        logging.info(f"Pausing execution for {pause_time_in_sec}s")
        time.sleep(pause_time_in_sec)
    else:
        pause_time_in_sec = random.randint(delay_min_sec, delay_max_sec)
        logging.info(f"Pausing execution for {pause_time_in_sec}s")
        time.sleep(pause_time_in_sec)
