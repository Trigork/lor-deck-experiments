import deckcoder

deep = "CICACAIFFAAQIBIPAIBAKCAKAQBAMJZPGU4AGAICAUDQEAIFDUXQKAQGC4OR4JJMAA"
very_short_bw = "CIAQ2AQGCQNB2JJHFEWC6NJWHA5TYAABAEBAMHQ"
lurk = "CMBAIBAGAEBQKDYGAQDRGFSBIRFFAAQCAQDAIBYCAQDTMRICAECAMAQBAQDTW"
thralls = "CMBQCAIBGIBQIBY7FRBAIBABAECQUDQDAEAQCFACAQAQMCIEAQDQ2SLIPAAQEBAHEI5Q"

decoded = deckcoder.decode_deck(deep)
classified = deckcoder.get_classified_decklist(decoded)
decklist = deckcoder.get_decklist(decoded)

for group,cards in classified.items():
    if len(cards) > 0:
        print(f"[{group.upper()}]")
    for quant,card in cards:
        print(f"({card['cost']}) {card['name']} [x{quant}]")

recoded = deckcoder.encode_deck(decoded)

print("Original: ", deep)
print("Re-Encoded: ", recoded)