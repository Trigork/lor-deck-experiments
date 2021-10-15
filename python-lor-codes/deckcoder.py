import base64
import math
import varint
from cardcodedb import carddb as cdb

CARDCODE_LENGTH = 7
MAX_KNOWN_VERSION = 4
FORMAT = 1
INITIAL_VERSION = 1

faction_library_version = {
    "DE" : 1,
    "FR" : 1,
    "IO" : 1,
    "NX" : 1,
    "PZ" : 1,
    "SI" : 1,
    "BW" : 2,
    "MT" : 2,
    "SH" : 3,
    "BC" : 4
}

def encode_deck (decklist : list) -> str:
    result = base64.b32encode(get_deck_bytes(decklist)).decode('utf-8').strip("=")
    return result

def decode_deck (code : str) -> list:
    deck = []
    
    pad_length = math.ceil(len(code) / 8) * 8 - len(code)
    padcode = code + '=' * pad_length
    deckbytes = base64.b32decode(padcode)

    bytelist = list(deckbytes)
    
    # grab format and version
    format = bytelist[0] >> 4
    version = bytelist[0] & 0xF
    del bytelist[0]

    for i in range(3):
        idx = 3-i
        num_group_ofs = varint.pop_varint(bytelist)
        
        for j in range(num_group_ofs):
            num_ofs_in_this_group = varint.pop_varint(bytelist)
            set = varint.pop_varint(bytelist)
            faction = varint.pop_varint(bytelist)

            for k in range(num_ofs_in_this_group):
                card = varint.pop_varint(bytelist)

                set_string = f'{set:02}'
                faction_string =  cdb.get_faction_code(faction)
                card_string = f'{card:03}'

                deck += [ (f"{set_string}{faction_string}{card_string}", idx)]

    # the remainder of the deck code is comprised of entries for cards with counts >= 4
    # this will only happen in Limited and special game modes.
    # the encoding is simply [count] [cardcode]
    while (len(bytelist) > 0):
        four_plus_count = varint.pop_varint(bytelist)
        four_plus_set = varint.pop_varint(bytelist)
        four_plus_faction = varint.pop_varint(bytelist)
        four_plus_number = varint.pop_varint(bytelist)

        four_plus_set_string = f'{four_plus_set:02}'
        four_plus_faction_string = cdb.get_faction_code(four_plus_faction)
        four_plus_card_string = f'{four_plus_number:03}'

        deck += [ (f"{four_plus_set_string}{four_plus_faction_string}{four_plus_card_string}", four_plus_count)]

    return deck

def get_deck_bytes(decklist: list) -> list:
    deck_bytes = []

    if not are_valid_cardcodes_and_counts(decklist):
        raise ValueError("The provided deck contains invalid card codes.")
    
    format_and_version = FORMAT << 4 | get_min_supported_library_version(decklist) & 0xF

    deck_bytes += [format_and_version]

    of3 = []
    of2 = []
    of1 = []
    ofN = []

    for cardcode,count in decklist:
        if count == 3:
            of3 += [(cardcode,count)]
        elif count == 2:
            of2 += [(cardcode,count)]
        elif count == 1:
            of1 += [(cardcode,count)]
        elif count < 1:
            raise ValueError(f"Invalid count of {count} for card {cardcode}")
        else:
            ofN += [(cardcode,count)]

    grouped_of3s = get_grouped_ofs(of3)
    grouped_of2s = get_grouped_ofs(of2)
    grouped_of1s = get_grouped_ofs(of2)

    grouped_of3s = sort_group_of(grouped_of3s)
    grouped_of2s = sort_group_of(grouped_of2s)
    grouped_of1s = sort_group_of(grouped_of1s)

    ofN = sorted(ofN, key=lambda e: e[0])

    # encode
    encode_group_of(deck_bytes, grouped_of3s)
    encode_group_of(deck_bytes, grouped_of2s)
    encode_group_of(deck_bytes, grouped_of1s)
    encode_nof(deck_bytes, ofN)

    return bytearray(deck_bytes)

def get_decklist(code_deck : dict) -> list:
    db_deck = []
    for card in code_deck:
        cd = cdb.get_card_data(card[0])
        db_deck += [(card[1], cd)]
    
    db_deck.sort(key=lambda x: x[1]["cost"])
    return db_deck

def get_classified_decklist(code_deck : dict) -> dict:
    classified_deck = { "champions" : [], "units" : [], "landmarks" : [], "spells" : [] }

    for card in code_deck:
        cd = cdb.get_card_data(card[0])
        if cd["type"] == "unit" and cd["supertype"] == "champion":
            classified_deck["champions"] += [(card[1], cd)]
        if cd["type"] == "unit" and cd["supertype"] != "champion":
            classified_deck["units"] += [(card[1], cd)]
        if cd["type"] == "spell":
            classified_deck["spells"] += [(card[1], cd)]
        if cd["type"] == "landmark":
            classified_deck["landmarks"] += [(card[1], cd)]
    
    for k in classified_deck.keys():
        classified_deck[k].sort(key=lambda x: x[1]["cost"])
    return classified_deck

def are_valid_cardcodes_and_counts(decklist: list) -> bool:
    for cardcode,count in decklist:
        if len(cardcode) != CARDCODE_LENGTH:
            return False
        try:
            int(cardcode[:2])
            f = cardcode[2:4]
            if not f in cdb.faction_codes.keys():
                return False
            int(cardcode[4:])
        except ValueError as e:
            return False
        if count < 1:
            return False
    return True

def get_min_supported_library_version(decklist: list) -> int:
    if len(decklist) == 0:
        return INITIAL_VERSION
    try:
        return max([faction_library_version[cardcode[2:4]] for cardcode,q in decklist])
    except Exception as e:
        return MAX_KNOWN_VERSION
        
def get_grouped_ofs(cardcodecount : list) -> list:
    groups = {}
    while len(cardcodecount) > 0:
        current_ccc = cardcodecount.pop(0)
        current_set_faction = current_ccc[0][0:4]
        if current_set_faction not in groups.keys():
            groups[current_set_faction] = [current_ccc]
        else:
            groups[current_set_faction] += [current_ccc]

        for idx,ccc in enumerate(cardcodecount):
            set_faction = ccc[0][0:4]
            if set_faction == current_set_faction:
                groups[current_set_faction] += [ccc]
                del cardcodecount[idx]
    return list(groups.values())

def sort_group_of(groups_of : list) -> list:
    groups_of = sorted(groups_of, key=lambda e: (len(e), e[0][0]))
    for i in range(len(groups_of)):
        groups_of[i] = sorted(groups_of[i], key=lambda e: e[0])
    return groups_of

def parse_card_code(code : str) -> tuple:
    set = int(code[:2])
    faction = code[2:4]
    id = int(code[4:])
    return (set, faction, id)

def encode_group_of(bytelist : list, group_of : list):
    bytelist += varint.get_varint(len(group_of))
    for current_list in group_of:
        # how many cards in group?
        bytelist += varint.get_varint(len(current_list))

        # what is this group?
        current_cardcode = current_list[0][0]
        setno, faction, number = parse_card_code(current_cardcode)
        faction_no = cdb.get_faction_id(faction)
        bytelist += varint.get_varint(setno)
        bytelist += varint.get_varint(faction_no)

        # what are the cards?
        for cardcode,count in current_list:
            number = int(cardcode[4:])
            bytelist += varint.get_varint(number)


def encode_nof(bytelist : list, nof : list):
    for ccc in nof:
        bytelist += varint.get_varint(len(nof))

        set_no, faction, number = parse_card_code(ccc[0])
        faction_no = cdb.get_faction_id(faction)

        bytelist += varint.get_varint(set_no)
        bytelist += varint.get_varint(faction_no)
        bytelist += varint.get_varint(number)