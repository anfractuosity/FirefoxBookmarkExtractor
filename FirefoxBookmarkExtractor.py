#!/usr/bin/python3

import sqlite3
import glob
import csv
import os
import argparse
import hashlib
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Directory containing places.sqlite")
parser.add_argument("download_dir", help="Directory to check for webpages and to write webpages to") 
parser.add_argument("csv", help="Filename for CSV output")                                                                                                                             
parser.parse_args()
args = parser.parse_args()

places = []
placeshash = {}

print("Now walking %s..." % (args.dir))

for root, dirs, files in os.walk(args.dir,followlinks=True):
    for file in files:
        if file == "places.sqlite":
            places.append(os.path.join(root, file))
print(places)

for p in places:
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * FROM moz_bookmarks AS a JOIN moz_places AS b ON a.fk = b.id')

    for r in c.fetchall():
        placeshash[r["url"]] = r["title"]

with open(args.csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

    for k,v in placeshash.items():
        h = hashlib.new('md5')
        h.update(k.encode("utf-8"))
        csvwriter.writerow([h.hexdigest(),k,v])
        
        urlfolder = h.hexdigest()

        wpage = os.path.join(args.download_dir,urlfolder)
        
        # Only download webpage if we don't have it already
        if not os.path.isdir(wpage):
            #print(urlfolder)
            if k.startswith("http"):
                print("Downloading ",k)            
                with open(os.devnull, 'w') as devnull:
                    completed = subprocess.run(['wget', '-T1','-t1','-E','-k','-H','-nd','-N','-p','-P'+wpage,k],stdout=devnull,stderr=devnull)
