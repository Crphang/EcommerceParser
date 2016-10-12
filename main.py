from bs4 import BeautifulSoup
import sys
import csv

def parse(base_url, html_text):
    print "Trying to parse"
    csv = "error"
    if ("amazon.com" in base_url):
        csv = parse_amazon(html_text)
    elif ("ebay.com" in base_url):
        csv = parse_ebay(html_text)
    return csv


#Input: HTML Text
#Output: "url,name,price" (if successful)
#        "error" (if fail)         
def parse_amazon(html_text):
    return "error"

#Input: HTML Text
#Output: "url,name,price" (if successful)
#        "error" (if fail) 
def parse_ebay(html_text):
	soup = BeautifulSoup(open("Untitled Document"))
	span = soup.find_all('span', attrs={'id':'prcIsum'})[0]
	name = soup.find_all('h1', attrs={'id':'itTitle')[0]
	if (len(name.contents) < 2 or len(span.contents) < 1)
		return "error"
	return name.contents[1] + "," + span.contents[0]

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Search Term Argument is Missing")
        sys.exit()
    file_name = sys.argv[1] + '.csv'
    with open(file_name, 'w+') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for line in sys.stdin:
            html_array = line.split("|urldelimit|")
            data = parse(html_array[0], html_array[1])
            if (data == "error"):
                continue
            else:
                csvwriter.writerows(data.split(","))


