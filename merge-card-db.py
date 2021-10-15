import os
import json
import requests
import wget
from shutil import copyfile

REDOWNLOAD = False

file_path = os.path.dirname(os.path.realpath(__file__))

sets_path =  os.sep.join([file_path, "sets"])
carddata_path = os.sep.join([sets_path, "card-data"])

if REDOWNLOAD:
    for setno in range(1,999):
        try:
            url = f'https://dd.b.pvp.net/latest/set{setno}-lite-en_us.zip'
            wget.download(url)
        except Exception as e:
            break

list_of_files = {}
for (dirpath, dirnames, filenames) in os.walk(sets_path):
    for filename in filenames:
        if filename.endswith('.json') and filename.startswith('set'): 
            fname = os.sep.join([dirpath, filename])
            fdataname = os.sep.join([carddata_path, filename])
            list_of_files[filename] = fdataname

            # Check if file exists in card-data
            if not os.path.exists(fdataname):
                copyfile(fname, fdataname)
            else:
                newsize = os.path.getsize(fname)
                ogsize = os.path.getsize(fdataname)

                # If file exists but filesize is bigger
                if (newsize > ogsize):
                    copyfile(fname, fdataname)

cardcode_db = {}
for fname,path in list_of_files.items():
    with open(path, encoding="utf8") as f:
        data = json.load(f)
        for card in data:
            cardcode_db.update({card["cardCode"] : {
                "name" : card["name"],
                "region" : card["region"],
                "cost" : card["cost"],
                "type" : card["type"].lower(),
                "supertype" : card["supertype"].lower()
                }
            })

outfile = os.sep.join([file_path, "cardcodedb.json"])
with open(outfile, 'w') as of:
    json.dump(cardcode_db, of, indent=4, sort_keys=True)



