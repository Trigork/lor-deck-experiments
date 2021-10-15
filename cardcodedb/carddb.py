import os
import json
import random

faction_codes = {
    "DE": 0,
    "FR": 1,
    "IO": 2,
    "NX": 3,
    "PZ": 4,
    "SI": 5,
    "BW": 6,
    "SH": 7,
    "MT": 9,
    "BC": 10
}

faction_indexes = {
    0: "DE",
    1: "FR",
    2: "IO",
    3: "NX",
    4: "PZ",
    5: "SI",
    6: "BW",
    7: "SH",
    9: "MT",
    10: "BC"
}

file_path = os.path.dirname(os.path.realpath(__file__))
db_path =  os.sep.join([file_path, "cardcodedb.json"])

card_db = {}
with open(db_path, encoding="utf8") as f:
    card_db = json.load(f)

def get_card_data(code: str) -> dict:
    return card_db[code]

def card_exists(code: str) -> bool:
    return code in card_db.keys()

def get_faction_code(faction_no : int) -> str:
    return faction_indexes[faction_no]

def get_faction_id(faction_code : str) -> int:
    return faction_codes[faction_code]

def get_random_cardcode() -> str:
    return random.choice(card_db.keys())