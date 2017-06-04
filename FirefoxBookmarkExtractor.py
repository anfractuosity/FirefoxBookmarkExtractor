#!/usr/bin/python3

import sqlite3
import glob
import csv
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Directory containing places.sqlite")
parser.add_argument("csv", help="Filename for CSV output")                                                                                                                             
parser.parse_args()
args = parser.parse_args()

places = []
placeshash = {}

print("Now walking %s..." % (args.dir))

for root, dirs, files in os.walk(args.dir):
    for file in files:
        if file == "places.sqlite":
            places.append(os.path.join(root, file))

for p in places:
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * FROM moz_bookmarks AS a JOIN moz_places AS b ON a.fk = b.id')

    for r in c.fetchall():
        placeshash[r["url"]] = r["title"]

with open(args.csv, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

    for k,v in placeshash.items():
        spamwriter.writerow([k,v])

