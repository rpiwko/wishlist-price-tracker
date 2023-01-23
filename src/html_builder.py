"""
Module for building HTML page
"""


import logging


good_value_class = "good-value"
bad_value_class = "bad-value"


def build_wishlist_items_table(objects_list):
    html_table = "<table id=\"wishlistItemsTable\">\n"
    html_table += "<h3>Wishlist items</h3>\n"

    # Build header
    html_table += "<tr><th>Category</th>"
    html_table += "<th>Title</th>"
    html_table += "<th>Author</th>"
    html_table += "<th>URL</th>"
    html_table += "<th>Available</th>"
    html_table += "<th>Lowest Price</th>"
    html_table += "<th>Latest Price</th>"
    html_table += "<th>Highest Price</th>"
    html_table += "<th>Comment</th>"
    html_table += "</tr>\n"

    # Add items
    for item in objects_list:
        offers_no = len(item["offers"])
        if offers_no == 1:
            html_table += f"<tr><td>{item['category']}</td>"
            html_table += f"<td><a href='{item['jsonFile']}'>{item['title']}</a></td>"
            html_table += f"<td>{item['author']}</td>"
        else:
            html_table += f"<tr><td rowspan={offers_no}>{item['category']}</td>"
            html_table += f"<td rowspan={offers_no}><a href='{item['jsonFile']}'>{item['title']}</a></td>"
            html_table += f"<td rowspan={offers_no}>{item['author']}</td>"

        for n in range(offers_no):
            if n > 0:
                html_table += "<tr>"
            offer = item["offers"][n]
            url = offer['url']
            html_table += f"<td><a href='{url}'>{_get_short_url(url)}</a></td>"
            html_table += get_is_available_cell(offer)
            html_table += get_cells_with_prices(offer)
            if n == 0:
                html_table += f"<td rowspan={offers_no}>{item['comment']}</td>"
            html_table += "</tr>\n"

        html_table = html_table.replace("<tr>", f"<tr class=\"{_format_category_name(item['category'])}\">")

    html_table += "</table>"
    logging.info("html_table=\n" + html_table)
    return html_table


def build_category_selector(objects_list):
    html_category_selector = "<div>\n"
    html_category_selector += "<h3>Categories</h3>\n"

    categories = ["All"] + _get_categories(objects_list)
    logging.info("Found categories: " + str(categories))

    for category in categories:
        formatted_category_name = _format_category_name(category)
        html_category_selector += f"<input type=\"radio\" name=\"category\" id=\"{formatted_category_name}\" onClick=\"showCategory('{formatted_category_name}')\">\n"
        html_category_selector += f"<label for=\"{formatted_category_name}\">{category}</label><br>\n"
        if category == "All":
            html_category_selector = html_category_selector.replace("type=\"radio\"", "type=\"radio\" checked")
        
    html_category_selector += "</div>"
    logging.info("html_category_selector=\n" + html_category_selector)
    return html_category_selector


def put_element_into_template(element, input_file_path, element_marker, output_file_path):
    logging.info("Reading input file: " + str(input_file_path))
    html_page = ""
    with open(input_file_path, "r") as input_file:
        html_page = input_file.read()
    html_page = html_page.replace(element_marker, element)
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
    lowest_price_cell = f"<td>{offer['lowestPrice']}</td>"
    latest_price_cell = f"<td>{offer['latestPrice']}</td>"
    highest_price_cell = f"<td>{offer['highestPrice']}</td>"
    if offer["isAvailable"]:
        try:
            # All three prices are equal -> no need to add any color
            if float(offer["lowestPrice"]) == float(offer["highestPrice"]):
                pass
            # Latest price is the lowest one -> GOOD
            elif float(offer["latestPrice"]) == float(offer["lowestPrice"]):
                latest_price_cell = latest_price_cell.replace("<td>", f"<td class=\"{good_value_class}\">")
                lowest_price_cell = lowest_price_cell.replace("<td>", f"<td class=\"{good_value_class}\">")
            # Latest price is the highest one -> BAD
            elif float(offer["latestPrice"]) == float(offer["highestPrice"]):
                latest_price_cell = latest_price_cell.replace("<td>", f"<td class=\"{bad_value_class}\">")
                highest_price_cell = highest_price_cell.replace("<td>", f"<td class=\"{bad_value_class}\">")
        except ValueError:
            pass
    return lowest_price_cell + latest_price_cell + highest_price_cell


def _get_short_url(url):
    short_url = url.removeprefix("https://").removeprefix("www.")
    short_url = short_url[:short_url.find("/")]
    return short_url


def _get_categories(objects_list):
    categories = []
    for object in objects_list:
        if not object["category"] in categories:
            categories.append(object["category"])
    return categories


def _format_category_name(category_name):
    return category_name.lower().strip().replace(" ", "-")