# What it is?
Simple CLI tool to monitor and compare prices in web stores.

# How to use it?

## 1. Find item which price you want to follow
Go to web store page, find item and save its URL. 
Check different stores to gather as many offers/URLs as possible.

Currently supported stores can be found in src/shop_watcher/shops directory.

## 2. Prepare configuration file for your item
Each monitored item has its own JSON configuration file under etc directory.
Create new file or copy and rename some existing one, or use one of prepared templates (tpl files under etc directory). 
Then enter found URLs into the item config file to get structure like below:  

```
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
            "highestPriceDate": null"
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
            "highestPriceDate": null"
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
            "highestPriceDate": null"
        }
}
```


## 3. Put the item config file to etc folder
Make sure item config file has *.json extension.
Make sure item config file is inside etc directory or inside one if its subdirectories. 

## 4. Execute bin/main_script.py
Main script will do the following:
- Read item configuration file
- Go to each URL to check item availability and its price in each store
- Update item config file with found details
- Generate HTML page with table containing all prices from all stores (my_wishlist.html inside out directory)

## 5. Further steps
- Prepare more configs to monitor as many items as you like.
- Add bin/main_script.py to cron for daily or weekly executing.
- Keep your eyes on generated HTML page as it will mark best/worst prices as well as the best offers ever.

# Technical details
Searching for price may fail due to:
- 404
- Exception when searching price and availability
- No exception but price not found (e.g. item is not available anymore)
