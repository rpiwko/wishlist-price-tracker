"""
Module for building HTML page
"""


import logging


def build_table_from_objects(objects_list):
    html_table = "<table>\n"

    # Build header
    html_table += "<tr><th>Title</th>"
    html_table += "<th>URL</th>"
    html_table += "<th>Available</th>"
    html_table += "<th>Latest Price</th>"
    html_table += "<th>Lowest Price</th>"
    html_table += "</tr>\n"

    # Add items
    for item in objects_list:
        offers_no = len(item["offers"])
        html_table += f"<tr><td rowspan={offers_no}>{item['title']}</td>"
        for offer in item["offers"]:
            url = offer['url']
            html_table += f"<td><a href='{url}'>{_get_short_url(url)}</a></td>"
            html_table += f"<td>{offer['isAvailable']}</td>"
            html_table += f"<td>{offer['latestPrice']}</td>"
            html_table += f"<td>{offer['lowestPrice']}</td></tr>\n"

    html_table += "</table>"
    logging.info("html_table=\n" + html_table)
    return html_table


def put_table_into_html_page(table, input_file_path, marker, output_file_path):
    logging.info("Reading input file: " + str(input_file_path))
    html_page = ""
    with open(input_file_path, "r") as input_file:
        html_page = input_file.read()
    html_page = html_page.replace(marker, table)
    with open(output_file_path, "w") as output_file:
        output_file.write(html_page)


def _get_short_url(url):
    short_url = url.removeprefix("https://").removeprefix("www.")
    short_url = short_url[:short_url.find("/")]
    return short_url
