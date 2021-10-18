from cardcodedb import carddb as cdb
from deckcoder import deckcoder
import random

class Card:
    set : int
    faction_no : int
    number: int

    def __init__(self, set, faction_no, number):
        self.set = set
        self.faction_no = faction_no
        self.number = number
    
    def __init__(self, card_code):
        self.set = int(card_code[:2])
        self.faction_no = cdb.get_faction_id(card_code[2:4])
        self.number = int(card_code[4:])
    
    def get_cardcode(self):
        return f"{self.set:02}{cdb.get_faction_code(self.faction_no)}{self.number:03}"

class CardAndQuantity:
    card : Card
    quantity : int

    def __init__(self, card, quantity=1):
        self.card = card
        self.quantity = quantity

    def __init__(self, set, faction_no, number, quantity=1):
        self.card = Card(set, faction_no, number)
        self.quantity = quantity

    def to_tuple(self):
        return (self.card.get_cardcode(), self.quantity)

class Individual:
    factions : list
    singles_decklist : list
    faction_mutation_chance : float
    card_mutation_chance: float

    def __init__(self, factions : list, singles_decklist : list, faction_mutation_chance=0.1, card_mutation_chance=0.05):
        self.factions = factions
        self.singles_decklist = singles_decklist
        self.faction_mutation_chance = faction_mutation_chance
        self.card_mutation_chance = card_mutation_chance
    
    def __str__(self):
        deck = compress_decklist(self.singles_decklist)
        code = deckcoder.encode_deck(deck)
        return f"[{self.factions[0]},{self.factions[1]}] {code}"
    
    def mutate(self):
        new_singles_decklist = self.singles_decklist
        for i,(c,q) in enumerate(self.singles_decklist):
            if (random.random() <= self.card_mutation_chance):
                new_code = cdb.get_random_cardcode_from_factions(self.factions)
                copies_in_deck = count_copies_in_deck(self.singles_decklist, new_code)
                # Only mutate to cards that won't exceed the playset count
                # If we collision with a card that we already have 3 of, bad luck, our card doesn't mutate
                if copies_in_deck < 3:
                    new_singles_decklist[i] = (new_code, 1)

            self.singles_decklist = new_singles_decklist
            self.factions = get_deck_factions(self.singles_decklist)

# Factions can be repeated so we can go from mono to dual and viceversa
def select_factions(count : int) -> list:
    factions = []
    for i in range(count):
        factions += [random.choice(list(cdb.faction_codes.keys()))]
    return factions

def get_deck_factions(decklist : list) -> list:
    mono_regions = set([])
    multi_regions = set([])
    for c,q in decklist:
        card_info = cdb.get_card_data(c)
        card_regions = card_info['region_codes']
        if len(card_regions) == 1:
            mono_regions.add(set(card_regions))
        else:
            multi_regions.add(set(card_regions))
    


def count_copies_in_deck(decklist : list, code : str) -> int:
    copies = 0
    for c,q in decklist:
        if c == code:
            copies += q
    return copies

def compress_decklist(deck : list) -> list:
    card_copies = {}
    idx = 0
    for card,copies in deck:
        if not card in card_copies.keys():
            card_copies[card] = copies
        else:
            card_copies[card] += copies
    return [(c,q) for c,q in card_copies.items()]

# Generate a 40-card list that allows repetition up to 3 of the same card
# These decklists are not valid decklists for the encoder so we have to compress them
# before encoding.
def generate_random_singles_list(faction1, faction2):
    cards_in_deck = 0
    decklist = []

    while cards_in_deck < 40:
        card = cdb.get_random_cardcode_from_factions([faction1, faction2])
        quantity = random.randint(1,3)
        copies_in_deck = count_copies_in_deck(decklist, card)
        addables = quantity - copies_in_deck
        for i in range(addables):
            decklist += [(card, 1)]

        cards_in_deck += addables

    return decklist

def generate_population(population_size, faction_mutation=0.1, card_mutation=0.05):
    population = []
    for i in range(population_size):
        factions = select_factions(2)
        sdeck = generate_random_singles_list(factions[0], factions[1])
        population += [Individual(factions, sdeck, faction_mutation, card_mutation)]
    return population

