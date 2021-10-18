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
    if code in card_db.keys():
        return card_db[code]
    else:
        raise ValueError(f"There is no card for cardcode {code}. Try updating the DB plugin.")

def card_exists(code: str) -> bool:
    return code in card_db.keys()

def get_faction_code(faction_no : int) -> str:
    if faction_no in faction_indexes.keys():
        return faction_indexes[faction_no]
    else:
        raise ValueError(f"Unknown Faction with ID: {faction_no}")

def get_faction_id(faction_code : str) -> int:
    if faction_code in faction_codes.keys():
        return faction_codes[faction_code]
    else:
        raise ValueError(f"Unknown Faction Code: {faction_code}")

def card_belongs_to_factions(code, factions):
    if card_exists(code):
        card = get_card_data(code)
        regions = set(card['region_codes'])
        s_factions = set(factions)
        count = len(regions.intersection(s_factions))
        if count >= 1:
            return True
        else:
            return False
    else:
        return False

def get_cards_from_factions(factions : list, allow_tokens=False) -> dict:
    return dict(filter(lambda elem: (card_belongs_to_factions(elem[0], factions)) and (not elem[1]['is_token'] or allow_tokens) , card_db.items()))

def get_cards_from_sets(set_ids : list, allow_tokens=False) -> dict:
    return dict(filter(lambda elem: int(elem[0][:2]) in set_ids and (not elem[1]['is_token'] or allow_tokens), card_db.items()))

def get_cards_from_sets_and_factions(set_ids : list, factions :list, allow_tokens=False) -> dict:
    return dict(filter(lambda elem: int(elem[0][:2]) in set_ids and (card_belongs_to_factions(elem[0], factions)) and (not elem[1]['is_token'] or allow_tokens), card_db.items()))

def get_random_cardcode() -> str:
    return random.choice(list(card_db.keys()))

def get_random_cardcode_from_factions(factions : list) -> str:
    return random.choice(list(get_cards_from_factions(factions).keys()))

def get_random_cardcode_from_sets(set_ids : list) -> str:
    return random.choice(list(get_cards_from_sets(set_ids).keys()))

def get_random_cardcode_from_sets_and_factions(set_ids : list, factions : list) -> str:
    return random.choice(list(get_cards_from_sets_and_factions(set_ids, factions).keys()))