import json
with open('public/data/research_data_1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
keys = list(data[0].keys())
with open('actual_keys_hex.txt', 'w', encoding='utf-8') as out:
    for key in keys:
        if "Link" in key:
            out.write(f"KEY: {repr(key)} HEX: {key.encode('utf-8').hex()}\n")
