"""
Module for building HTML page
"""


import logging


good_value_class = "good-value"
bad_value_class = "bad-value"
empty_value = "-"


def build_wishlist_items_table(objects_list):
    html_table = "<table id=\"wishlistItemsTable\">\n"
    html_table += "<h3>Wishlist items</h3>\n"

    # Build the header
    html_table += "<thead><tr><th>Category</th>"
    html_table += "<th>Title</th>"
    html_table += "<th>Author</th>"
    html_table += "<th>URL</th>"
    html_table += "<th>Available</th>"
    html_table += "<th>Lowest Price</th>"
    html_table += "<th>Latest Price</th>"
    html_table += "<th>Highest Price</th>"
    html_table += "<th>Comment</th>"
    html_table += "</tr></thead>\n"

    # Add items
    for item in objects_list:
        logging.info("Processing item: " + item['title'])
        offers_no = len(item["offers"])
        logging.info(f"Offers number: {offers_no}")
        if offers_no <= 1:
            html_table += f"<tbody><tr><td>{item['category']}</td>"
            html_table += f"<td><a href='{item['jsonFile']}'>{item['title']}</a></td>"
            html_table += f"<td>{item['author']}</td>"
        else:
            html_table += f"<tbody><tr><td rowspan={offers_no}>{item['category']}</td>"
            html_table += f"<td rowspan={offers_no}><a href='{item['jsonFile']}'>{item['title']}</a></td>"
            html_table += f"<td rowspan={offers_no}>{item['author']}</td>"

        best_price_today, worst_price_today = _get_best_and_worst_prices_today(item)
        logging.info(f"best_price_today={best_price_today}")
        logging.info(f"worst_price_today={worst_price_today}")

        if offers_no == 0:
            html_table += f"<td>{empty_value}</td>"
            html_table += f"<td class=\"{bad_value_class}\">No</td>"
            html_table += f"<td>{empty_value}</td>"
            html_table += f"<td>{empty_value}</td>"
            html_table += f"<td>{empty_value}</td>"
            html_table += "<td></td>"
            html_table += "</tr></tbody>\n"
        else:
            for n in range(offers_no):
                if n > 0:
                    html_table += "<tr>"
                offer = item["offers"][n]
                url = offer['url']
                html_table += f"<td><a href='{url}'>{_get_short_url(url)}</a></td>"
                html_table += _get_is_available_cell(offer)
                html_table += _get_cells_with_prices(offer, best_price_today, worst_price_today)
                if n == 0:
                    comment = item['comment']
                    if _is_best_price_ever(best_price_today, item):
                        comment = "BEST PRICE EVER!" + "<br><br>" + comment if comment else "BEST PRICE EVER!"
                    html_table += f"<td rowspan={offers_no}>{comment}</td>"
                html_table += "</tr>"
            html_table += "</tbody>\n"

        html_table = html_table.replace("<tbody>", f"<tbody class=\"{_format_category_name(item['category'])}\">")

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


def _get_is_available_cell(offer):
    if offer['isAvailable']:
        cell = f"<td class=\"{good_value_class}\">Yes</td>"
    else:
        cell = f"<td class=\"{bad_value_class}\">No</td>"
    return cell


def _get_cells_with_prices(offer, best_price_for_item, worst_price_for_item):
    if offer['lowestPrice']:
        lowest_price_cell = f"<td>{float(offer['lowestPrice']):.2f}</td>"
    else:
        lowest_price_cell = f"<td>{empty_value}</td>"
    if offer['latestPrice']:
        latest_price_cell = f"<td>{float(offer['latestPrice']):.2f}</td>"
    else:
        latest_price_cell = f"<td>{empty_value}</td>"
    if offer['highestPrice']:
        highest_price_cell = f"<td>{float(offer['highestPrice']):.2f}</td>"
    else:
        highest_price_cell = f"<td>{empty_value}</td>"
    if offer["isAvailable"]:
        try:
            if float(offer["latestPrice"]) == best_price_for_item:
                logging.info(f"The latestPrice={offer['latestPrice']} is today the best one!")
                latest_price_cell = latest_price_cell.replace("<td>", f"<td class=\"{good_value_class}\">")
            elif float(offer["latestPrice"]) == worst_price_for_item:
                logging.info(f"The latestPrice={offer['latestPrice']} is today the worst one!")
                latest_price_cell = latest_price_cell.replace("<td>", f"<td class=\"{bad_value_class}\">")
        except ValueError as e:
            logging.error(f"Error while preparing price cells for offer {offer['url']}:\n{e}")
            pass
    return lowest_price_cell + latest_price_cell + highest_price_cell


def _get_short_url(url):
    short_url = url.removeprefix("https://").removeprefix("www.")
    short_url = short_url[:short_url.find("/")]
    return short_url


def _get_best_and_worst_prices_today(item):
    best_price_today = None
    worst_price_today = None
    for offer in item["offers"]:
        if offer["latestPrice"] and offer["isAvailable"]:
            if best_price_today is None or best_price_today > float(offer["latestPrice"]):
                best_price_today = float(offer["latestPrice"])
            if worst_price_today is None or worst_price_today < float(offer["latestPrice"]):
                worst_price_today = float(offer["latestPrice"])
    return best_price_today, worst_price_today


def _is_best_price_ever(best_price_today, item):
    if best_price_today is None:
        return False
    lowest_among_lowest_prices = None
    for offer in item["offers"]:
        if offer["lowestPrice"]:
            if lowest_among_lowest_prices is None or lowest_among_lowest_prices > float(offer["lowestPrice"]):
                lowest_among_lowest_prices = float(offer["lowestPrice"])
    logging.info(f"lowest_among_lowest_prices={lowest_among_lowest_prices}")
    if lowest_among_lowest_prices is not None and best_price_today <= lowest_among_lowest_prices:
        logging.info(f"Best price ever!")
        return True
    else:
        return False


def _get_categories(objects_list):
    categories = []
    for object in objects_list:
        if not object["category"] in categories:
            categories.append(object["category"])
    return categories


def _format_category_name(category_name):
    return category_name.lower().strip().replace(" ", "-")
