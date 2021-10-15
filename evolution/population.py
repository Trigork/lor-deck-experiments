
from cardcodedb import carddb as cdb

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


print(cdb.get_random_cardcode())


        
        


