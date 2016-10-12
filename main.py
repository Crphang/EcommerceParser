from bs4 import BeautifulSoup

def parse(base_url, html_text):
    print "Trying to parse"
    csv = "error"
    if (base_url == "amazon.com"):
        csv = parse_amazon(html_text)
    else if (base_url == "ebay.com"):
        csv = parse_ebay(html_text)


def parse_amazon(html_text):
    return "<replace_url>,<replace_name>,<replace_price>"

def parse_ebay(html_text):
    return "<replace_url>,<replace_name>,<replace_price>"

if __name__ == "__main__":
