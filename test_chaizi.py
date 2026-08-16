from hanzi_chaizi import HanziChaizi
hc = HanziChaizi()
out = f"的: {hc.query('的')}\n明: {hc.query('明')}\n休: {hc.query('休')}\n"
with open('test_chaizi.txt', 'w', encoding='utf-8') as f:
    f.write(out)
