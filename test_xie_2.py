import bs4
import json

def extract():
    with open('xiehanzi.html', 'r', encoding='utf-8') as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
        
    def get_section(title_text):
        heading = soup.find(lambda tag: tag.name in ['h2', 'h3'] and title_text.lower() in tag.text.lower())
        if not heading:
            return "NOT FOUND"
        
        # In a shadcn/ui Card, heading is in a div.flex, content is in the next div
        header_div = heading.parent
        if header_div:
            content_div = header_div.find_next_sibling('div')
            if content_div:
                # return all text inside content_div
                return content_div.get_text(separator=' | ', strip=True)
        return "NO SIBLING"

    res = {
        "Bo thu": get_section('Bộ thủ'),
        "Han Viet": get_section('Hán-Việt'),
        "Tu nguyen": get_section('Tự nguyên'),
        "De nham": get_section('Dễ nhầm'),
        "Lien quan": get_section('Liên quan')
    }
    
    with open('out_xie_2.json', 'w', encoding='utf-8') as out:
        json.dump(res, out, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    extract()
