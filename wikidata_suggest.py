#!/usr/bin/env python

import re
import sys
import json
import time
import requests

from colorama import Fore, Style, init

cache = {}

def suggest(orig_name):
    name = orig_name
    if name in cache:
        return cache[name]

    init()

    while True:

        print
        print(Fore.RED + name + Style.RESET_ALL)
        print

        suggestions = _wikidata(name)

        count = 0
        for s in suggestions['search']:
            count += 1
            label = s.get('label', '')
            description = s.get('description', 'https:' + s['url'])

            print(Fore.BLUE + str(count) + ')' + ' ' + Style.BRIGHT + label),
            if description:
                print(' - ' + description),
            print(Fore.RESET)

        gs = None
        if count == 0:
            gs = _google(name)
            if gs:
                print(Fore.MAGENTA + 'G)' + ' google suggests: ' + gs + Fore.RESET)

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
            r = suggestions['search'][int(choice)-1]
            cache[orig_name] = r
            return r
        elif gs and choice[0] == "G": 
            name = gs
        elif choice[0] == "O":
            name = raw_input("Lookup: ")
        elif choice[0] == "N":
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
            "limit": "25"
        }
        return requests.get(url, params=params).json()


def _google(name, sleep=1):
    url = 'http://ajax.googleapis.com/ajax/services/search/web'
    ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'}
    params = {'v': '1.0', 'q': name}
    response = requests.get(url, params=params, headers=ua).json()
    if response["responseStatus"] != 200:
        print "received error (%s) from google, waiting %s seconds" % (response["responseStatus"], sleep)
        time.sleep(sleep)
        return _google(name, sleep * 2)
    for result in response['responseData']['results']:
        if 'wikipedia.org/wiki/' in result['unescapedUrl']:
            parts = [s.strip() for s in result['titleNoFormatting'].split(' - ')]
            # remove parenthetical content
            name = parts[0]
            name = re.sub(' \(.+\)', '', name)
            return name
    return None


class Quit(Exception):
    pass
