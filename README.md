# FirefoxBookmarkExtractor

Extract bookmarks from a directory which contains multiple places.sqlite files, then outputs unique URLs to a CSV

```
usage: FirefoxBookmarkExtractor.py [-h] dir csv

positional arguments:
  dir         Directory containing places.sqlite
  csv         Filename for CSV output

optional arguments:
  -h, --help  show this help message and exit
```

# ToDo

Write script to then grab all websites from the bookmark list, in an efficient fashion (including page content such as images etc).
