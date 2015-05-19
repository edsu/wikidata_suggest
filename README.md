# wikidata_suggest

`wikidata_suggest` is a simple command line tool for interactively reconciling 
your data against [Wikidata](https://wikidata.org). Once you've installed it
you will get a command line tool `wd` for querying Wikidata, which lets you 
look up something:

If nothing is found at Wikidata it will go and look for a Wikipedia result in
the first page of results at Google, and give you an opportunity to use that
instead.

Most likely though you will want to use wikidata_suggest as a little data
cleansing/augmentation library. For example if you have a CSV spreadsheet 
that has an *author* column that you'd like to link up to Wikidata.

```python

import csv

from wikidata_suggest import suggest

reader = csv.reader(open("data.csv"))
writer = csv.writer(open("new_data.csv", "wb"))

for row in reader:
  # column 2 has author names
  wd = suggest(row[1])
  if wd:
    row.append(wd["id"])
  else:
    row.append(None)
```


