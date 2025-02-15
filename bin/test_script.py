"""
Testing script
"""


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.joinpath("../src")))
from logging_setup import initialize_logging
import shop_watcher as shop_watcher


print("Script started...")

log_files_dir = Path(__file__).parent.joinpath("../logs")
initialize_logging(log_files_dir, __file__)

print("##### Test get_the_price()")
results = shop_watcher.get_the_price("https://www.nexto.pl/ebooki/hobbit,_czyli_tam_i_z_powrotem_p1249864.xml")
print("nexto.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://www.nexto.pl/ebooki/zbyt_wielcy_by_upasc_p34300.xml")
print("nexto.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.planszomania.pl/karciane/4983/Marvel-Legendary:-Deck-Building-Game.html")
print("planszomania.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://www.planszomania.pl/przygodowe/22609/Deep-Madness-edycja-polska.html")
print("planszomania.pl - not available item w promo: " + str(results))
results = shop_watcher.get_the_price("https://www.planszomania.pl/strategiczne/25596/Black-Rose-Wars-edycja-podstawowa.html")
print("planszomania.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://virtualo.pl/ebook/hobbit-czyli-tam-i-z-powrotem-i360890/")
print("virtualo.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://virtualo.pl/ebook/biala-bluzka-i7148/")
print("virtualo.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://virtualo.pl/ebook/przygody-dobrego-wojaka-szwejka-czasu-wojny-swiatowej-i239153/")
print("virtualo.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.publio.pl/hobbit-j-r-r-tolkien,p87958.html")
print("publio.pl - available item w promo: " + str(results))
results = shop_watcher.get_the_price("https://www.publio.pl/mock-marek-krajewski,p846772.html")
print("publio.pl - available item w/o promo: " + str(results))
results = shop_watcher.get_the_price("https://www.publio.pl/noce-i-dnie-tomy-1-4-maria-dabrowska,p183324.html")
print("publio.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://ebookpoint.pl/ksiazki/po-pismie-jacek-dukaj,e_12my.htm#format/e")
print("ebookpoint.pl - available item w promo: " + str(results))
results = shop_watcher.get_the_price("https://ebookpoint.pl/ksiazki/powierniczka-opowiesci-sally-page,e_2xk9.htm")
print("ebookpoint.pl - available item w/o promo: " + str(results))
results = shop_watcher.get_the_price("https://ebookpoint.pl/ksiazki/spiacy-giganci-sylvain-neuvel,e_0b1m.htm#format/e")
print("ebookpoint.pl - not available item and product page available: " + str(results))
results = shop_watcher.get_the_price("https://ebookpoint.pl/ksiazki/anne-z-zielonych-szczytow-lucy-maud-montgomery,e_2cpa.htm")
print("ebookpoint.pl - not available item and product page not available: " + str(results))
results = shop_watcher.get_the_price("https://ebookpoint.pl/ksiazki/anomalia-herv-le-tellier,e_26d4.htm")
print("ebookpoint.pl - available item but other format not available: " + str(results))
results = shop_watcher.get_the_price("https://woblink.com/ebook/polmistrz-mariusz-czubaj-268504u")
print("woblink.com - available item w promo: " + str(results))
results = shop_watcher.get_the_price("https://woblink.com/ebook/zly-tyrmand-mariusz-urbanek-252420u")
print("woblink.com - available item w/o promo: " + str(results))
results = shop_watcher.get_the_price("https://woblink.com/ksiazka/sienkiewicz-polityczny-sienkiewicz-ideologiczny--56343")
print("woblink.com - not available item: " + str(results))
results = shop_watcher.get_the_price("https://fortgier.pl/p/16/26671/-uszkodzona-nato-the-cold-war-goes-hot-designer-signature-edition-czasy-wspolczesne-wojenne-i-historyczne-gry.html")
print("fortgier.pl - available item w promo: " + str(results))
results = shop_watcher.get_the_price("https://fortgier.pl/p/83/24909/b-17-flying-fortress-leader-2nd-edition-solitaire-gry.html")
print("fortgier.pl - available item w/o pro: " + str(results))
results = shop_watcher.get_the_price("https://bonito.pl/produkt/nocny-obserwator")
print("bonito.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://bonito.pl/produkt/uratowane-z-potopu--dvd-2")
print("bonito.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://bonito.pl/produkt/pociagniecie-piora-zagubione-opowiadania")
print("bonito.pl - preorder: " + str(results))
results = shop_watcher.get_the_price("https://www.taniaksiazka.pl/zgroza-w-dunwich-i-inne-przerazajace-opowiesci-howard-phillips-lovecraft-p-1739149.html")
print("taniaksiazka.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://www.taniaksiazka.pl/the-thing-on-the-doorstep-and-other-weird-stories-howard-phillips-lovecraft-p-1763985.html")
print("taniaksiazka.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.taniaksiazka.pl/dom-usherow-p-1964911.html")
print("taniaksiazka.pl - preorder: " + str(results))
results = shop_watcher.get_the_price("https://vesper.pl/weird-fiction/1210-zgroza-w-dunwich-i-inne-przerazajace-opowiesci-wyd2022-howard-phillips-lovecraft-oprawa-twarda-9788377314456.html")
print("vesper.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://vesper.pl/beletrystyka/1170-piaty-kier-dan-simmons-oprawa-twarda-9788377314364.html")
print("vesper.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://vesper.pl/zapowiedzi/1365-wieczny-wojownik-t-1-michael-moorcock-oprawa-twarda-9788377315101.html")
print("vesper.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.gildia.pl/komiksy/225003-straznicy")
print("gildia.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://www.gildia.pl/komiksy/251627-v-jak-vendetta")
print("gildia.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.gildia.pl/literatura/370689-uratowane-z-potopu")
print("gildia.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://mystic.pl/product-pol-59358-Unleashed-No-Sign-Of-Life-CD-LIMITED.html")
print("mystic.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://mystic.pl/product-pol-71106-Vanilla-Fudge-Spirit-Of-67.html")
print("mystic.pl - preorder: " + str(results))
results = shop_watcher.get_the_price("https://mystic.pl/product-pol-28910-Tristania-Rubicon-Limited-Edition.html")
print("mystic.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://komiksiarnia.pl/sandman/15190-smierc-wydiii-9788328157408.html")
print("komiksiarnia.pl - available: " + str(results))
results = shop_watcher.get_the_price("https://komiksiarnia.pl/aliens-vs-predator/10055-aliens-vs-predator-30th-anniversary-edition-9788366291515.html")
print("komiksiarnia.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://planszostrefa.pl/pl/p/Thunderbolt-Apache-Leader/2337")
print("planszostrefa.pl - available: " + str(results))
results = shop_watcher.get_the_price("https://planszostrefa.pl/pl/p/Legendary-Encounters-An-Alien-Deck-Building-Game/3675")
print("planszostrefa.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.swiatksiazki.pl/emma-6749841-e-book.html")
print("swiatksiazki.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://www.swiatksiazki.pl/dziennik-1943-1948-6337276-e-book.html")
print("swiatksiazki.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://strefamarzen.pl/pl/products/d-d-ghost-of-saltmarsh-board-game-dodatek-13907")
print("strefamarzen.pl - available: " + str(results))
results = shop_watcher.get_the_price("https://strefamarzen.pl/pl/products/the-thing-gra-planszowa-edycja-polska-14487")
print("strefamarzen.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://aleplanszowki.pl/przygodowe/9358-waste-knights-druga-edycja--5902259206446.html")
print("aleplanszowki.pl - available: " + str(results))
results = shop_watcher.get_the_price("https://aleplanszowki.pl/strategiczne/8083-legendary-encounters-an-alien-deck-building-game-edycja-angielska.html")
print("aleplanszowki.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://aleplanszowki.pl/lord-of-the-rings-lcg/16939-the-lord-of-the-rings-the-card-game-the-dream-chaser-hero-expansion-edycja-angielska.html")
print("aleplanszowki.pl - removed item: " + str(results))
results = shop_watcher.get_the_price("https://www.dvdmax.pl/my-dying-bride-the-ghost-of-orion-cd,art1058972")
print("dvdmax.pl - available: " + str(results))
results = shop_watcher.get_the_price("https://www.dvdmax.pl/my-dying-bride-for-darkest-eyes-black-2xwinyl,art1766664")
print("dvdmax.pl - available: " + str(results))
results = shop_watcher.get_the_price("https://www.dvdmax.pl/my-dying-bride-the-manuscript-winyl,art311569")
print("dvdmax.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://dragoneye.pl/diuna-imperium-p-2925.html")
print("dragoneye.pl - available: " + str(results))
results = shop_watcher.get_the_price("https://dragoneye.pl/legendary-encounters-an-alien-deck-building-game-eng-p-2151.html")
print("dragoneye.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://mepel.pl/diuna-imperium-edycja-polska")
print("mepel.pl - available: " + str(results))
results = shop_watcher.get_the_price("https://mepel.pl/tainted-grail-the-fall-of-avalon-echoes-of-the-past-edycja-polska")
print("mepel.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://mepel.pl/iss-vanguard-core-pledge-polska-edycja-gamefound")
print("mepel.pl - preorder: " + str(results))
results = shop_watcher.get_the_price("https://mangastore.pl/miecz-niesmiertelnego-1-oprawa-twarda-p-4611.html")
print("mangastore.pl - available: " + str(results))
results = shop_watcher.get_the_price("https://mangastore.pl/miecz-niesmiertelnego-6-oprawa-twarda-preorder-p-5495.html")
print("mangastore.pl - preorder: " + str(results))
results = shop_watcher.get_the_price("https://mangastore.pl/ghost-in-the-shell-1-p-699.html")
print("mangastore.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://mangarden.pl/pl/products/akira-edycja-specjalna-tom-01-12386.html")
print("mangarden.pl - available: " + str(results))
results = shop_watcher.get_the_price("https://mangarden.pl/pl/products/akira-edycja-specjalna-tom-04-12389.html")
print("mangarden.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.x-kom.pl/p/1051543-smartfon-telefon-xiaomi-poco-x4-gt-8-256gb-black.html")
print("x-kom.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://www.x-kom.pl/p/1070549-smartfon-telefon-sony-xperia-5-iv-zielony.html")
print("x-kom.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.rebel.pl/gry-planszowe/everdell-edycja-polska-109580.html")
print("rebel.pl - available item: " + str(results))
results = shop_watcher.get_the_price("https://www.rebel.pl/gry-planszowe/aliens-bug-hunt-2002009.html")
print("rebel.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://www.rebel.pl/ksiazki/thorgal-tom-15-wladca-gor-101912.html")
print("rebel.pl - not available item and product page not available: " + str(results))
results = shop_watcher.get_the_price("https://lostintime.pl/sklep/komiksy/fantasy/toppi-kolekcja-tom-2-ameryka-polnocna/")
print("lostintime.pl - available item, no promo: " + str(results))
results = shop_watcher.get_the_price("https://lostintime.pl/sklep/komiksy/fantasy/legenda-o-szkarlatnych-oblokach-wydanie-zbiorcze/")
print("lostintime.pl - available item, promo: " + str(results))
results = shop_watcher.get_the_price("https://lostintime.pl/sklep/komiksy/obyczajowe/wypadek-na-polowaniu/")
print("lostintime.pl - not available item: " + str(results))
results = shop_watcher.get_the_price("https://lostintime.pl/sklep/komiksy/przygodowe/hitomi/")
print("lostintime.pl - preorder: " + str(results))

print("Script completed!")