import os
import json
import requests
from shutil import copyfile
import argparse

region_codes = {
    "Demacia" : "DE",
    "Freljord" : "FR",
    "Noxus" : "NX",
    "PiltoverZaun" : "PZ",
    "ShadowIsles" : "SI",
    "Targon" : "MT",
    "BandleCity" : "BC",
    "Bilgewater" : "BW",
    "Shurima" : "SH",
    "Ionia" : "IO"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--locale", type=str, default="en_us", help="Sets the locale of the DB files downloaded")
    args = parser.parse_args()

    file_path = os.path.dirname(os.path.realpath(__file__))

    set_data = {}
    for setno in range(1,999):
        try:
            url = f'https://dd.b.pvp.net/latest/set{setno}/{args.locale.lower()}/data/set{setno}-{args.locale.lower()}.json'
            resp = requests.get(url=url)
            data = resp.json()
            set_data[setno] = data
        except Exception as e:
            break

    cardcode_db = {}
    for set_cards in set_data.values():
        for card in set_cards:
            cardcode_db.update({card["cardCode"] : {
                "name" : card["name"],
                "region" : card["region"],
                "region_codes" : [ region_codes[r] for r in card["regionRefs"] ],
                "cost" : card["cost"],
                "type" : card["type"].lower(),
                "supertype" : card["supertype"].lower(),
                "is_token" : not card["collectible"]
                }
            })

    outfile = os.sep.join([file_path, "cardcodedb.json"])
    with open(outfile, 'w') as of:
        json.dump(cardcode_db, of, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()