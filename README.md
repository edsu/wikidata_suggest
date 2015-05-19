# wikidata_suggest

`wikidata_suggest` is a simple command line tool for interactively reconciling 
your data against [Wikidata](https://wikidata.org). First you'll want to
install:

    % pip install wikidata_suggest

Once you've installed it you will get a command line tool `wd`:

![](http://edsu.github.io/wikidata_suggest/images/screenshot1.png)

If nothing is found at Wikidata `wd` will automatically go and look for a 
Wikipedia result in the first page of results at Google, and give you an 
opportunity to use that instead.

![](http://edsu.github.io/wikidata_suggest/images/screenshot2.png)

Most likely you will want to use wikidata_suggest as a little data 
cleansing/augmentation library. For example if you have a CSV spreadsheet 
that has an *author* column that you'd like to link up to Wikidata, you 
can do something like this:

```python

import csv

from wikidata_suggest import suggest

reader = csv.reader(open("data.csv"))
writer = csv.writer(open("new_data.csv", "wb"))

# read the csv 
for row in reader:

  # column 2 has author names
  author = row[1]

  # drop into interactive session
  wikidata = suggest(author)

  if wikidata:
    row.append(wikidata["id"])
  else:
    row.append(None)
  
  # write our new row 
  writer.writerow(row)

reader.close()
writer.close()
```


