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
	soup = BeautifulSoup(open("script.html")) # need to change
	# find name
	seivedMeta = soup.find_all('meta', attrs={'name':'title'})
	text = str(seivedMeta[0])
	text = text.replace(":", "|")
	name = text.split('|')
	name = name[1].strip()

	# find price
	seivedSpan =soup.find_all('span', attrs={'id':'miniATF_price'})
	if(len(seivedSpan) == 0):
		return "error"

	value=  str(seivedSpan[0].contents[0]).strip()
	# remove dash if value is a range etc, $3.00 - $6.00
	removedDash = value.split('-')

	if(removedDash[0].find('$') == -1):
		return "error"

	# only 1 price, not a range
	elif(len(removedDash) ==1):
		firstVal = removedDash[0]
		firstVal = (firstVal.split('$'))[1] # extract the numbers
		mean = float(firstVal)
		# return format = name, value, mean
		# example: name, 43.00, 43.00		
		return name + "," + firstVal + "," + firstVal

	# range of prices
	else:
		firstVal = removedDash[0].strip()
		secondVal = removedDash[1].strip()
		firstVal = (firstVal.split('$'))[1]
		secondVal = (secondVal.split('$'))[1]
		mean = (float(firstVal)+float(secondVal))/2.0
		# return format = name, range, mean
		# return example: name, 40.00 - 60.00, 50.00
	    	return name + "," + firstVal + "-" + secondVal + "," + mean



#Input: HTML Text
#Output: "url,name,price" (if successful)
#        "error" (if fail) 
def parse_ebay(html_text):
	soup = BeautifulSoup(open("Untitled Document"))
	span = soup.find_all('span', attrs={'id':'prcIsum'})[0]
	name = soup.find_all('h1', attrs={'id':'itemTitle'})[0]
	if (len(name.contents) < 2 or len(span.contents) < 1):
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


