# lor-deckcoder

Code repo to host some experiments with coding and decoding Legends of Runeterra deck codes

- deckcoder: a python library to encode and decode decks
- cardcodedb: a module to download, merge and mantain a json cardcode database
- evolution: genetic algorithms to try and get longest and shortest possible deck codes

A cardcodedb.json file is required for everything to work properly, this file is bundled with the project, but it can be
created by running ```python cardcodedb/create-carddb.py```. This script requests the card info from Riot's servers and
creates the local cardcodedb.json file, always updated to the latest version of the game. You can specify a card locale with
```python cardcodedb/create-carddb.py -l <locale>```. Uses en_us locale by default.

Samples of how to import and use the cardcodedb and deckcoder modules can be found in evolution/population.py