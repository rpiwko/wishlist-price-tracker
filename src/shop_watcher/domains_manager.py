"""
Supported domains management module
"""


import shop_watcher.string_tools as string_tools


# TODO: Import shops dynamically, remove hardcoded supported_domains
supported_domains = {
    "nexto.pl": "nexto", 
    "publio.pl": "publio",
    "virtualo.pl": "virtualo"}


def validate_domain(url):
    """
    Checks whether URL domain is supported

    Args:
        url (str): URL to validate
    """
    url_domain = string_tools.get_domain_from_url(url)
    accepted_domains = list(supported_domains.keys())
    if url_domain not in accepted_domains:
        raise ValueError(f"Unexpected URL domain detected: '{url_domain}'. Accepted domains are: {accepted_domains}")
