#!/usr/bin/env python

import re
import sys
import json
import time
import requests

from colorama import Fore, Style, init

cache = {}

def suggest(orig_name):

    name = orig_name.strip()

    if name == None or name == "":
        return None

    if name in cache:
        return cache[name]

    init()

    while True:

        print
        print(Fore.RED + 'Search: ' + name + Style.RESET_ALL)
        print

        # print wikidata suggestions
        wd_sug = _wikidata(name)

        count = 0
        for s in wd_sug['search']:
            count += 1
            label = s.get('label', '')
            description = s.get('description', 'https:' + s['url'])

            print(Fore.BLUE + str(count) + ')' + ' ' + Style.BRIGHT + label),
            if description:
                print(' - ' + description),
            print(Fore.RESET)

        # print wikipedia suggestions
        wp_sug = _wikipedia(name)
        if wp_sug:
            print(Fore.MAGENTA + 'W) Wikipedia suggests %s' % wp_sug + Fore.RESET)

        print(Fore.GREEN + 'N) none')
        print(Fore.YELLOW + 'O) other')
        print(Fore.RED + 'Q) quit')
        print(Style.RESET_ALL)

        try:
            choice = raw_input("Choice: ")
        except EOFError:
            print
            return None

        choice = choice.upper()
        if re.match('^\d+$', choice):
            r = wd_sug['search'][int(choice)-1]
            cache[orig_name] = r
            cache[name] = r
            return r
        elif wp_sug and choice[0] == "W": 
            name = wp_sug
        elif choice[0] == "O":
            name = raw_input("Lookup: ")
        elif choice[0] == "N":
            cache[orig_name] = None
            cache[name] = None
            return None
        elif choice[0] == "Q":
            raise Quit()


def _wikidata(name):
        url = "http://www.wikidata.org/w/api.php"
        params = {
            "search": name,
            "action": "wbsearchentities",
            "format": "json",
            "language": "en",
            "type": "item",
            "continue": "0",
            "limit": "10"
        }
        return requests.get(url, params=params).json()


def _wikipedia(name, lang='en'):
    url = "https://%s.wikipedia.org/w/api.php" % lang
    params = {
        "action": "query",
        "list": "search",
        "format": "json",
        "srnamespace": "0",
        "srsearch": name
    }
    sug = None
    results = requests.get(url, params=params).json()
    if len(results['query']['search']) > 0:
        sug = results['query']['search'][0]['title']
    elif 'suggestion' in results['query']['searchinfo'] and \
            name != results['query']['searchinfo']['suggestion']:
        sug = _wikipedia(results['query']['searchinfo']['suggestion'], lang)
    return sug

class Quit(Exception):
    pass
