#!/usr/bin/env python

import json
from wikidata_suggestor import suggest

name = raw_input("Search: ")
print json.dumps(suggest(name), indent=2)
