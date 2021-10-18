import pytest
import base64
from deckcoder import deckcoder
import math

class Helpers:
    @staticmethod
    def verify_rehydration(deck, rehydrated) -> bool:
        if (len(deck) != len(rehydrated)):
            return False
        
        for cd,q in rehydrated:
            found = False
            for deckcd,deckq in deck:
                if (deckcd == cd and deckq == q):
                    found = True
                    break
        
            if not found:
                return False
        
        return True
    
    @staticmethod
    def extract_version_from_deckcode(code : str) -> int:
        deck = []
        pad_length = math.ceil(len(code) / 8) * 8 - len(code)
        padcode = code + '=' * pad_length
        deckbytes = base64.b32decode(padcode)
        bytelist = list(deckbytes)
        return bytelist[0] & 0xF

class TestDeckCoder:
    @pytest.fixture()
    def sample_decklists(self, shared_datadir):
        lines = (shared_datadir / 'decklists.txt').read_text().splitlines()
        sample_decks = { }
        current_deckcode = ""
        for l in lines:
            code = l.strip('\n').strip()
            if code == "":
                pass
            if not ':' in code:
                if code != '':
                    sample_decks[code] = []
                    current_deckcode = code
            else:
                if current_deckcode != '':
                    q,cardcode = code.split(':')
                    q = int(q)
                    sample_decks[current_deckcode] += [(cardcode, q)]
        return sample_decks

    def test_encode_recommended_decks(self, sample_decklists):
        for code,deck in sample_decklists.items():
            encoded = deckcoder.encode_deck(deck)
            assert code == encoded

    def test_small_deck(self):
        decklist = []
        decklist += [('01DE002', 1)]

        code = deckcoder.encode_deck(decklist)
        decoded = deckcoder.decode_deck(code)

        assert True == Helpers.verify_rehydration(decklist, decoded)
    
    def test_large_deck(self):
        decklist = []
        decklist += [('01DE002', 3)]
        decklist += [('01DE003', 3)]
        decklist += [('01DE004', 3)]
        decklist += [('01DE005', 3)]
        decklist += [('01DE006', 3)]
        decklist += [('01DE007', 3)]
        decklist += [('01DE008', 3)]
        decklist += [('01DE009', 3)]
        decklist += [('01DE010', 3)]
        decklist += [('01DE011', 3)]
        decklist += [('01DE012', 3)]
        decklist += [('01DE013', 3)]
        decklist += [('01DE014', 3)]
        decklist += [('01DE015', 3)]
        decklist += [('01DE016', 3)]
        decklist += [('01DE017', 3)]
        decklist += [('01DE018', 3)]
        decklist += [('01DE019', 3)]
        decklist += [('01DE020', 3)]
        decklist += [('01DE021', 3)]

        code = deckcoder.encode_deck(decklist)
        decoded = deckcoder.decode_deck(code)

        assert True == Helpers.verify_rehydration(decklist, decoded)

    def test_deck_with_counts_more_than3_small(self):
        decklist = []
        decklist += [('01DE002', 4)]

        code = deckcoder.encode_deck(decklist)
        decoded = deckcoder.decode_deck(code)

        assert True == Helpers.verify_rehydration(decklist, decoded)
    
    def test_deck_with_counts_more_than3_large(self):
        decklist = []
        decklist += [('01DE002', 3)]
        decklist += [('01DE003', 3)]
        decklist += [('01DE004', 3)]
        decklist += [('01DE005', 3)]
        decklist += [('01DE006', 4)]
        decklist += [('01DE007', 5)]
        decklist += [('01DE008', 6)]
        decklist += [('01DE009', 7)]
        decklist += [('01DE010', 8)]
        decklist += [('01DE011', 9)]
        decklist += [('01DE012', 3)]
        decklist += [('01DE013', 3)]
        decklist += [('01DE014', 3)]
        decklist += [('01DE015', 3)]
        decklist += [('01DE016', 3)]
        decklist += [('01DE017', 3)]
        decklist += [('01DE018', 3)]
        decklist += [('01DE019', 3)]
        decklist += [('01DE020', 3)]
        decklist += [('01DE021', 3)]

        code = deckcoder.encode_deck(decklist)
        decoded = deckcoder.decode_deck(code)

        assert True == Helpers.verify_rehydration(decklist, decoded)

    def test_single_card_40_times(self):
        decklist = []
        decklist += [('01DE002', 40)]
        code = deckcoder.encode_deck(decklist)
        decoded = deckcoder.decode_deck(code)

        assert True == Helpers.verify_rehydration(decklist, decoded)
    
    def test_worst_case_length(self):
        decklist = []
        decklist += [('01DE002', 4)]
        decklist += [('01DE003', 4)]
        decklist += [('01DE004', 4)]
        decklist += [('01DE005', 4)]
        decklist += [('01DE006', 4)]
        decklist += [('01DE007', 5)]
        decklist += [('01DE008', 6)]
        decklist += [('01DE009', 7)]
        decklist += [('01DE010', 8)]
        decklist += [('01DE011', 9)]
        decklist += [('01DE012', 4)]
        decklist += [('01DE013', 4)]
        decklist += [('01DE014', 4)]
        decklist += [('01DE015', 4)]
        decklist += [('01DE016', 4)]
        decklist += [('01DE017', 4)]
        decklist += [('01DE018', 4)]
        decklist += [('01DE019', 4)]
        decklist += [('01DE020', 4)]
        decklist += [('01DE021', 4)]

        code = deckcoder.encode_deck(decklist)
        decoded = deckcoder.decode_deck(code)

        assert True == Helpers.verify_rehydration(decklist, decoded)
    
    def test_invariant_order(self):
        deck1 = []
        deck1 += [('01DE002', 1)]
        deck1 += [('01DE003', 2)]
        deck1 += [('02DE003', 3)]

        deck2 = []
        deck2 += [('01DE003', 2)]
        deck2 += [('02DE003', 3)]
        deck2 += [('01DE002', 1)]

        code1 = deckcoder.encode_deck(deck1)
        code2 = deckcoder.encode_deck(deck2)

        assert code1 == code2

        deck3 = []
        deck3 += [('01DE002', 4)]
        deck3 += [('01DE003', 2)]
        deck3 += [('02DE003', 3)]

        deck4 = []
        deck4 += [('01DE003', 2)]
        deck4 += [('02DE003', 3)]
        deck4 += [('01DE002', 4)]

        code3 = deckcoder.encode_deck(deck3)
        code4 = deckcoder.encode_deck(deck4)

        assert code3 == code4
    
    def test_invariant_order2(self):
        deck1 = []
        deck1 += [('01DE002', 4)]
        deck1 += [('01DE003', 2)]
        deck1 += [('02DE003', 3)]
        deck1 += [('01DE004', 5)]

        deck2 = []
        deck2 += [('01DE004', 5)]
        deck2 += [('01DE003', 2)]
        deck2 += [('02DE003', 3)]
        deck2 += [('01DE002', 4)]

        code1 = deckcoder.encode_deck(deck1)
        code2 = deckcoder.encode_deck(deck2)

        assert code1 == code2
    
    def test_bilgewater_set(self):
        deck = []
        deck += [('01DE002', 4)]
        deck += [('02BW003', 2)]
        deck += [('02BW010', 3)]
        deck += [('01DE004', 5)]

        code = deckcoder.encode_deck(deck)
        decoded = deckcoder.decode_deck(code)

        assert True == Helpers.verify_rehydration(deck, decoded)
    
    def test_shurima_set(self):
        deck = []
        deck += [('01DE002', 4)]
        deck += [('02BW003', 2)]
        deck += [('02BW010', 3)]
        deck += [('04SH047', 5)]

        code = deckcoder.encode_deck(deck)
        decoded = deckcoder.decode_deck(code)

        assert True == Helpers.verify_rehydration(deck, decoded)
    
    def test_mttargon_set(self):
        deck = []
        deck += [('01DE002', 4)]
        deck += [('03MT003', 2)]
        deck += [('03MT010', 3)]
        deck += [('02BW004', 5)]

        code = deckcoder.encode_deck(deck)
        decoded = deckcoder.decode_deck(code)

        assert True == Helpers.verify_rehydration(deck, decoded)
    
    def test_bad_version(self):
        deck = []
        deck += [('01DE002', 4)]
        deck += [('01DE003', 2)]
        deck += [('02DE003', 3)]
        deck += [('01DE004', 5)]

        bytes_from_deck = list(base64.b32decode(deckcoder.encode_deck(deck)))
        bytes_from_deck[0] = 0x58

        with pytest.raises(ValueError) as e_info:
            bad_version_deck_code = base64.b32encode(bytearray(bytes_from_deck)).decode('utf-8').strip("=")
            deck_bad = deckcoder.decode_deck(bad_version_deck_code)
            expected = "The provided code requires a higher version of this library; please update."
            exception_msg = str(e_info)
            assert expected == exception_msg
            
    def test_bad_card_codes(self):
        deck = []
        deck += [('01DE02', 1)]
        with pytest.raises(ValueError) as e_info:
            code = deckcoder.encode_deck(deck)

        failed = False
        deck = []
        deck += [('01XX002', 1)]  
        with pytest.raises(ValueError) as e_info:
            code = deckcoder.encode_deck(deck)

        failed = False
        deck = []
        deck += [('01DE002', 0)]
        with pytest.raises(ValueError) as e_info:
            code = deckcoder.encode_deck(deck)
        
    def test_bad_count(self):
        failed = False
        deck = []
        deck += [('01DE002', 0)]  
        with pytest.raises(ValueError) as e_info:
            code = deckcoder.encode_deck(deck)

        deck = []
        deck += [('01DE002', -1)]  
        with pytest.raises(ValueError) as e_info:
            code = deckcoder.encode_deck(deck)
    
    def test_garbage_decoding(self):
        not_base32 = "I'm no card code!"
        bad_base32 = "ABCDEFG"
        bad_empty = ""

        with pytest.raises(ValueError) as e_info:
            deckcoder.decode_deck(not_base32)

        with pytest.raises(ValueError) as e_info:
            deckcoder.decode_deck(bad_base32)

        with pytest.raises(ValueError) as e_info:
            deckcoder.decode_deck(bad_empty)
    
    @pytest.mark.parametrize("config", [("DE",1), ("FR", 1), ("IO",1), ("NX", 1), ("PZ",1), ("SI", 1),
        ("BW",2), ("MT", 2), ("SH",3), ("BC", 4)])
    def test_deckversion_is_minimum_libraryversion_that_supports_the_contianed_factions(self, config):
        faction = config[0]
        version = config[1]

        decklist = []
        decklist += [('01DE001', 1)]
        decklist += [(f'01{faction}002', 1)]
        decklist += [(f'01FR001', 1)]

        code = deckcoder.encode_deck(decklist)

        minversion = Helpers.extract_version_from_deckcode(code)

        assert version == minversion
    
    def test_fail_futureversion(self):
        single_card_deck_version5 = "CUAAAAIBAUAAC"

        with pytest.raises(ValueError) as e_info:
            deckcoder.decode_deck(single_card_deck_version5)



        