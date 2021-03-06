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
#Output: "url,name,image,price,mean" (if successful)
#        "error" (if fail)         
def parse_amazon(html_text):
	soup = BeautifulSoup(open("script.html")) # need to change
	# find name
	seivedMeta = soup.find_all('meta', attrs={'name':'title'})
	text = str(seivedMeta[0])
	text = text.replace(":", "|")
	name = text.split('|')
	name = name[1].strip()

	# find image
	seivedImage = soup.findAll('img', {"data-a-dynamic-image":True} ) 
	img = seivedImage[0]['data-a-dynamic-image']
	end = img.split('"')
	img = end[1]

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
		# example: name, image, 43.00, 43.00		
		return name + "," +img + "," + firstVal + "," + firstVal

	# range of prices
	else:
		firstVal = removedDash[0].strip()
		secondVal = removedDash[1].strip()
		firstVal = (firstVal.split('$'))[1]
		secondVal = (secondVal.split('$'))[1]
		mean = (float(firstVal)+float(secondVal))/2.0
		# return format = name, range, mean
		# return example: name, image, 40.00 - 60.00, 50.00
	    	return name +"," + img + "," + firstVal + "-" + secondVal + "," + mean

#Input: HTML Text
#Output: "url,name,image,price,mean" (if successful)
#        "error" (if fail)  

#find title
def parse_lazada(html_text):
	seivedMeta = soup.find_all('title')
	name = str(seivedMeta).split(">")[1]
	name = name.split("|")[0].strip()

	#find image
	seivedMeta = soup.find_all('meta', attrs={'itemprop':'image'})
	lastMeta = None
	for lastMeta in seivedMeta:pass
	if lastMeta:
		image = lastMeta
	image = str(image).split("\"")[1]

	#find price
	seivedSpan = soup.find_all('span', attrs={'id':'special_price_box'})
	if(len(seivedSpan) == 0):
		print "error: no price found"
	price = str(seivedSpan[0].contents[0])
		
	return name +"," + image + "," + price + "," + price


#Input: HTML Text
#Output: "url,name,price" (if successful)
#        "error" (if fail) 

def parse_rakuten(html_text):
	#find title
	seivedTitle = soup.find_all('title')
	name = str(seivedTitle).split(":")[1].strip()
	name = name.split("<")[0]

	#find image
	seivedImage = soup.find_all('img', attrs={'id':'main_image'})
	image = str(seivedImage).split("src=\"")[1]
	image = image.split("\"")[0]
	
	#find price
	seivedPrice = soup.find_all('span', attrs={'id':'price_in_dollars'})
	price = str(seivedPrice).split("\\n")[1].strip()
	return name +"," + image + "," + price + "," + price



#Input: HTML Text
#Output: "url,name,price" (if successful)
#        "error" (if fail) 
def parse_ebay(html_text):
	soup = BeautifulSoup(open("Untitled Document"))
	span = soup.find_all('span', attrs={'id':'prcIsum'})[0]
	name = soup.find_all('h1', attrs={'id':'itemTitle'})[0]
	img = soup.findAll('img', {'id':'icImg'})[0]
	if (len(name.contents) < 2 or len(span.contents) < 1):
		return "error"
	return name.contents[1] + "," + img.get('src') + "," + span.contents[0] + "-" + span.contents[0] + "," + span.contents[0]


#Input: HTML Text
#Output: "url,name,price" (if successful)
#        "error" (if fail) 
def parse_zalora(html_text):
	try:
		soup = BeautifulSoup(open("Untitled Document 10"))
		discountPrice = soup.find_all('span', attrs={'class':'js-detail_updateSku_lowestPrice'})
		if(len(discountPrice) < 1):
			price = soup.find_all('span', attrs={'class':'value'})[0]	
		else:
			price = discountPrice[0].find_all('span', attrs={'class':'value'})[0]
		name = soup.find_all('div', attrs={'itemprop':'name'})[0]
		img = soup.find_all('img', attrs={'itemprop':'image'})[0]
		if (len(name.contents) < 1):
			return "error"
		return name.contents[0] + "," + str(img.get('src')).split("ffffff)/")[1] + "," + str(price.contents[0]) + " - " + str(price.contents[0]) + "," + str(price.contents[0])
	except:
		return "error"

#Input: HTML Text
#Output: "url,name,price" (if successful)
#        "error" (if fail) 
def parse_carousell(html_text):
	try:
		soup = BeautifulSoup(open("Untitled Document"))
		price = soup.find_all('meta', attrs={'property':'product:price:amount'})
		name = soup.find_all('title', attrs={'data-react-helmet':'true'})[0]
		#img = soup.find_all('div', attrs={'class':'swiper-wrapper'})
		img = soup.find_all('img')
		if (len(name.contents) < 1):
			return "error"
		return name.contents[0] + "," + img[0].get('data-layzr') + "," + str(price[0].get('content')) + " - " + str(price[0].get('content')) + "," + str(price[0].get('content'))
	except:
		return "error"

#Input: HTML Text
#Output: "url,name,price" (if successful)
#        "error" (if fail) 
def parse_aliexpress(html_text):
	soup = BeautifulSoup(open("Untitled Document 3"))
	tempPrice = soup.find_all('span', attrs={'itemprop':'lowPrice'})
	if (len(tempPrice)== 0):
		lowPrice = soup.find_all('span', attrs={'itemprop':'price'})[0]
		highPrice = lowPrice			
	else:
		highPrice = soup.find_all('span', attrs={'itemprop':'highPrice'})[0]
		lowPrice = tempPrice[0]
	name = soup.find_all('h1', attrs={'itemprop':'name'})[0]
	img = soup.findAll('img', {'alt':name.contents[0]})[0]
	mean = (float(lowPrice.contents[0]) + float(highPrice.contents[0])) / 2.0
	if (len(name.contents) < 1 or lowPrice.contents[0] < 0 or highPrice.contents[0] < 0):
		print "error"
	return name.contents[0] + "," + img.get('src') + "," + lowPrice.contents[0] + "-" + highPrice.contents[0] + "," + mean

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
	    print(data)
            if (data == "error"):
                continue
            else:
                csvwriter.writerows(data.split(","))


