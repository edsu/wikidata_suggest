#!/usr/bin/env python

import re
import sys
import json
import requests

from colorama import Fore, Style, init




def suggest(name):
    init()

    while True:

        print
        print(Fore.RED + name + Style.RESET_ALL)
        print

        suggestions = _wikidata(name)
        google_suggestion = _google(name)

        count = 0
        for s in suggestions['search']:
            count += 1
            label = s.get('label', '')
            description = s.get('description', '')
            print(Fore.BLUE + str(count) + ')' + ' ' + Style.BRIGHT + label + ': ' + description + Fore.RESET)

        if google_suggestion and google_suggestion.lower() != name.lower():
            print(Fore.MAGENTA + 'G)' + ' google suggests: ' + google_suggestion + Fore.RESET)

        print(Fore.GREEN + 'N) none')
        print(Fore.GREEN + 'O) other')
        print(Fore.RED + 'Q) quit')
        print(Style.RESET_ALL)

        try:
            choice = raw_input("Choice: ")
        except EOFError:
            print
            return None

        choice = choice.upper()
        if re.match('^\d+$', choice):
            return suggestions['search'][int(choice)-1]
        elif choice[0] == "G": 
            name = google_suggestion
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
            "continue": "0"
        }
        return requests.get(url, params=params).json()


def _google(name):
    url = 'http://ajax.googleapis.com/ajax/services/search/web'
    ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
    params = {'v': '1.0', 'q': name}
    response = requests.get(url, params=params, headers=ua).json()
    for result in response['responseData']['results']:
        if 'wikipedia.org/wiki/' in result['unescapedUrl']:
            parts = [s.strip() for s in result['titleNoFormatting'].split('-')]
            return parts[0]
    return None


class Quit(Exception):
    pass
