from hanzi_chaizi import HanziChaizi
hc = HanziChaizi()

def get_components(char):
    try:
        res = hc.query(char)
    except:
        return [char]
        
    if not res or res == [char]:
        return [char]
        
    components = []
    for c in res:
        # Prevent infinite recursion if a character breaks down into itself
        if c == char:
            components.append(c)
        else:
            components.extend(get_components(c))
    return components

out = f"的 breakdown: {hc.query('的')}\n"
out += f"的 components: {get_components('的')}\n"

out += f"想 breakdown: {hc.query('想')}\n"
out += f"想 components: {get_components('想')}\n"

with open('test_components.txt', 'w', encoding='utf-8') as f:
    f.write(out)
