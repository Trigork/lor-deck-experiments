import os
import json
import zipfile
import wget
from shutil import copyfile

REDOWNLOAD = True

file_path = os.path.dirname(os.path.realpath(__file__))
sets_path =  os.sep.join([file_path, "sets"])
codesets_path =  os.sep.join([file_path, "code_sets"])

if not os.path.exists(sets_path):
    os.mkdir(sets_path)

if not os.path.exists(codesets_path):
    os.mkdir(codesets_path)

if REDOWNLOAD:
    for setno in range(1,999):
        try:
            setname = f'set{setno}-lite-en_us'
            fname = f'{setname}.zip'
            url = f'https://dd.b.pvp.net/latest/{fname}'
            outfile = os.sep.join([sets_path, fname])
            outdir = os.sep.join([sets_path, setname])
            wget.download(url, out=outfile)
            with zipfile.ZipFile(outfile, 'r') as zip_ref:
                zip_ref.extractall(outdir)
            print()
        except Exception as e:
            break

list_of_files = {}
for (dirpath, dirnames, filenames) in os.walk(sets_path):
    for filename in filenames:
        if filename.endswith('.json') and filename.startswith('set'): 
            fname = os.sep.join([dirpath, filename])
            fdataname = os.sep.join([codesets_path, filename])
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



