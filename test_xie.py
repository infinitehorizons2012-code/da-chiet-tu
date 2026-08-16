import bs4

def extract():
    with open('xiehanzi.html', 'r', encoding='utf-8') as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
        
    def get_section(title_text):
        heading = soup.find(lambda tag: tag.name in ['h2', 'h3'] and title_text.lower() in tag.text.lower())
        if not heading:
            return "NOT FOUND"
        
        # We also want to capture a bit of HTML to know exactly how to parse it, 
        # so let's get the parent div that contains the heading
        return str(heading.parent)

    with open('out_xie.txt', 'w', encoding='utf-8') as out:
        out.write("Bộ thủ:\n" + get_section('Bộ thủ') + "\n\n")
        out.write("Hán Việt:\n" + get_section('Hán-Việt') + "\n\n")
        out.write("Tự nguyên:\n" + get_section('Tự nguyên') + "\n\n")
        out.write("Dễ nhầm:\n" + get_section('Dễ nhầm') + "\n\n")
        out.write("Liên quan:\n" + get_section('Liên quan') + "\n\n")

if __name__ == '__main__':
    extract()
