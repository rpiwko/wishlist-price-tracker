"""
Supported domains management module
"""


import logging
import shop_watcher.string_tools as string_tools
import shop_watcher


domains_vs_modules = {}


def get_shop_module_for_domain(domain):
    if domain in domains_vs_modules.keys():
        return domains_vs_modules[domain]
    else:
        raise ValueError("Module not found for domain: " + domain)


def import_shop_modules():
    global domains_vs_modules
    import os
    import importlib
    for file in os.listdir(os.path.dirname(__file__) + "/shops/"):
        if file.endswith(".py") and file != "base_shop.py":
            shop_name = file[:-3]
            module_name = "shop_watcher.shops." + shop_name
            # print(f"Loading module '{module_name}' for shop '{shop_name}'")
            globals()[module_name] = importlib.import_module(module_name)
            namespace_for_exec = dict()
            exec(f"domain_name = {module_name}.{shop_name}().get_supported_domain()", globals(), namespace_for_exec)
            domains_vs_modules[namespace_for_exec["domain_name"]] = module_name
    # print(str(domains_vs_modules))


def validate_domain(domain):
    """
    Checks whether domain is supported

    Args:
        url (str): Domain to validate. Use string_tools.get_domain_from_url(url) in order to extract domain from URL
    """
    if domain not in domains_vs_modules.keys():
        error_text = f"Unexpected URL domain detected: '{domain}'. Accepted domains are: {list(domains_vs_modules.keys())}"
        logging.error(error_text)
        raise ValueError(error_text)
