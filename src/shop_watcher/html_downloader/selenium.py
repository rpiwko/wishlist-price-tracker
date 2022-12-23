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


# Delays range used to avoid being banned
delay_min_sec = 2
delay_max_sec = 6

# How long WebDriver will poll DOM for element_to_wait
implicit_wait_in_seconds = 10


def get_the_html(url, element_to_wait=None):
    # TODO: Consider removing ignore_response_codes parameter
    # TODO: Add mechanism do automatic retry
    """
    Downloads HTML from URL

    Args:
        url (str): web page address to get the HTML from
        element_to_wait (str): xpath pointing page element for which WebDriver will wait before reading the html

    Returns:
        BeautifulSoup object created with "html.parser" and representing HTML page
    """
    logging.info("START: html_downloader.selenium.get_the_html()")
    logging.info(f"URL={url}")

    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service("/usr/local/bin/geckodriver", log_path="geckodriver.log"), # TODO: Parametrize the log path
                            options=firefox_options)
    driver.implicitly_wait(implicit_wait_in_seconds)

    try:
        driver.get(url)
        if element_to_wait:
            driver.find_element(By.XPATH, element_to_wait)
        raw_html_string = driver.page_source
        return  BeautifulSoup(raw_html_string, "html.parser")
    finally:
        driver.quit()
        logging.info("END: html_downloader.selenium.get_the_html()")


def get_htmls(url_list, element_to_wait=None):
    #TODO: Optimize to create only one driver instance for all URLs
    urls_with_htmls = {}
    for url in url_list:
        urls_with_htmls[url] = get_the_html(url, element_to_wait=element_to_wait)
        if url_list.index(url) < len(url_list) - 1:
            _pause_execution()
    return urls_with_htmls


def _pause_execution(pause_time_in_sec=0):
    if pause_time_in_sec:
        logging.info(f"Pausing execution for {pause_time_in_sec}s")
        time.sleep(pause_time_in_sec)
    else:
        pause_time_in_sec = random.randint(delay_min_sec, delay_max_sec)
        logging.info(f"Pausing execution for {pause_time_in_sec}s")
        time.sleep(pause_time_in_sec)
