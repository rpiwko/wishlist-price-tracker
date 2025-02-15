# What is it?

A simple CLI tool to monitor and compare prices in online stores.

# How to use it?

## 1. Find the item you want to track

Go to an online store, find the item, and save its URL. Check different stores to gather as many offers/URLs as possible.

Currently supported stores can be found in the `src/shop_watcher/shops` directory.

## 2. Prepare a configuration file for your item

Each monitored item has its own JSON configuration file stored in the `etc` directory. Create a new file, or copy and rename an existing one, or use one of the prepared templates (`tpl` files in the `etc` directory). Then, enter the collected URLs into the item configuration file to get a structure like the one below:

```json
{
    "title": "Hobbit",
    "category": "Books",
    "author": "J.R.R. Tolkien",
    "comment": "",
    "offers": [
        {
            "url": "https://bonito.pl/produkt/hobbit-wersja-ilustrowana-3",
            "isAvailable": true,
            "isAvailableDate": null,
            "lowestPrice": null,
            "lowestPriceDate": null,
            "latestPrice": null,
            "latestPriceDate": null,
            "highestPrice": null,
            "highestPriceDate": null
        },
        {
            "url": "https://www.taniaksiazka.pl/ksiazka/hobbit-wersja-ilustrowana-j-r-r-tolkien",
            "isAvailable": true,
            "isAvailableDate": null,
            "lowestPrice": null,
            "lowestPriceDate": null,
            "latestPrice": null,
            "latestPriceDate": null,
            "highestPrice": null,
            "highestPriceDate": null
        },
        {
            "url": "https://www.swiatksiazki.pl/hobbit-wersja-ilustrowana-6977680-ksiazka.html",
            "isAvailable": true,
            "isAvailableDate": null,
            "lowestPrice": null,
            "lowestPriceDate": null,
            "latestPrice": null,
            "latestPriceDate": null,
            "highestPrice": null,
            "highestPriceDate": null
        }
    ]
}
```

## 3. Place the item configuration file in the `etc` folder

- Ensure the configuration file has a `.json` extension.
- Make sure the file is inside the `etc` directory or one of its subdirectories.

## 4. Execute `bin/main_script.py`

The main script will perform the following actions:

- Read the item configuration file.
- Visit each URL to check item availability and pricing in each store.
- Update the item configuration file with the retrieved details.
- Generate an HTML page (`my_wishlist.html` inside the `out` directory) containing a table with all prices from all stores.

## 5. Next steps

- Prepare additional configuration files to monitor as many items as you like.
- Add `bin/main_script.py` to a cron job for daily or weekly execution.
- Regularly check the generated HTML page, as it will highlight the best and worst prices as well as historical best offers.

# Technical details

Price retrieval may fail due to:

- HTTP 404 errors.
- Exceptions when fetching price and availability data.
- No exceptions, but price not found (e.g. the item is no longer available).

