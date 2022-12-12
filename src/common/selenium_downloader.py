"""
Module to gather download functionalities for dynamic web pages. 
Handles requests and responses.
"""


import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


def get_the_html(url):
    """
    Downloads HTML from URL

    Args:
        url (str): web page address to get the HTML from

    Returns:
        HTML string downloaded from URL
    """
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service("/usr/local/bin/geckodriver", log_path="geckodriver.log"), # TODO: Parametrize the log path
                            options=firefox_options)
    driver.get(url)
    raw_html_string = driver.page_source
    logging.info(raw_html_string)
    driver.quit()
    return  BeautifulSoup(raw_html_string, "html.parser")
