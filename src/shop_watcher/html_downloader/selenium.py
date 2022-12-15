"""
HTML downloader for dynamic pages
"""


import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# How long WebDriver will poll DOM for element_to_wait
implicit_wait_in_seconds = 10


def get_the_html(url, element_to_wait=None):
    """
    Downloads HTML from URL

    Args:
        url (str): web page address to get the HTML from
        element_to_wait (str): xpath pointing page element for which WebDriver will wait before reading the html

    Returns:
        HTML string downloaded from URL
    """
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service("/usr/local/bin/geckodriver", log_path="geckodriver.log"), # TODO: Parametrize the log path
                            options=firefox_options)
    driver.implicitly_wait(implicit_wait_in_seconds)
    driver.get(url)
    if element_to_wait:
        driver.find_element(By.XPATH, element_to_wait)
    raw_html_string = driver.page_source
    # logging.info(raw_html_string)
    driver.quit()
    return  BeautifulSoup(raw_html_string, "html.parser")
