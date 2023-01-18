"""
Module for building HTML page
"""


import logging


good_value_class = "good-value"
bad_value_class = "bad-value"


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
            html_table += get_is_available_cell(offer)
            html_table += get_cells_with_prices(offer)
            html_table += "</tr>\n"

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


def get_is_available_cell(offer):
    cell = ""
    if offer['isAvailable']:
        cell = f"<td class=\"{good_value_class}\">Yes</td>"
    else:
        cell = f"<td class=\"{bad_value_class}\">No</td>"
    return cell

def get_cells_with_prices(offer):
    cell = f"<td>{offer['latestPrice']}</td>"
    cell += f"<td>{offer['lowestPrice']}</td>"
    try:
        if offer["isAvailable"] and float(offer["latestPrice"]) == float(offer["lowestPrice"]):
            cell = cell.replace("<td>", f"<td class=\"{good_value_class}\">")
        if float(offer["latestPrice"]) > float(offer["lowestPrice"]):
            cell = cell.replace("<td>", f"<td class=\"{bad_value_class}\">")
    except ValueError:
        pass
    return cell


def _get_short_url(url):
    short_url = url.removeprefix("https://").removeprefix("www.")
    short_url = short_url[:short_url.find("/")]
    return short_url
