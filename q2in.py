import requests
from bs4 import BeautifulSoup
import csv
myFile = open('output/in_book.csv','w')
with myFile:
	writer = csv.writer(myFile,delimiter=";")
	listt = ["Name","URL","Author","Price","Number of Ratings","Average Rating"]
	writer.writerow(listt)

def dv_spider(max_pages):
	i=1
	while i<=max_pages:
		myFile = open('output/in_book.csv','a')
		url = 'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg='+str(i)+'&ajax=1'
		source_code = requests.get(url)
		plain_text = source_code.text
		soup = BeautifulSoup(plain_text,"html.parser")
		lower = 'https://www.amazon.in'
		URL = []
		book_title = []
		Author = []
		Price = []
		nrating = []
		avgrating = []
		for containers in soup.findAll('div','zg_itemWrapper'):
					link = containers.find('a', 'a-link-normal')
					if link != None:
						linkk = link.get('href')
						URL.append("".join(lower+linkk))
					else:
						URL.append("Not available")

					text=containers.find('div', 'p13n-sc-truncate p13n-sc-line-clamp-1')
					if text != None:
						title = text.string
						title = title.split(' ')
						while '' in title:
							title.pop(title.index(''))
						title = ' '.join(title)
						title = title.strip('\n')
						book_title.append(str(title))
					else:
						book_title.append("Not available")
					
					contain=containers.find('div','a-section a-spacing-none p13n-asin')
					name = contain.find('a', 'a-size-small a-link-child')
					name1 = contain.find('span','a-size-small a-color-base')
					if name != None:
						author = name.string
					elif name1 != None:
						author = name1.string
					else:
						author = "Not available"
					Author.append(author)				
					
					contain=containers.find('span','p13n-sc-price')
					if contain != None:
						price = contain.text
						price = price.strip('\xa0').strip(' ')
						if price!=None:
							Price.append("Rs."+price)
						else:
							Price.append("Not available")
					else:
						Price.append("Not available")

					link=containers.find('a','a-size-small a-link-normal')
					if link != None:
						nrating.append(link.string)
					else:
						nrating.append("Not available")

					links=containers.find('div','a-icon-row a-spacing-none')
					if links != None:
						link = links.find('span','a-icon-alt')
						if link != None:
							avgrating.append(link.string)
						else:
							avgrating.append("Not available")
					else:
						avgrating.append("Not available")
		with myFile:
			writer = csv.writer(myFile,delimiter=";")
			input = list(zip(book_title,URL,Author,Price,nrating,avgrating))
			writer.writerows(input)
		i+=1
dv_spider(5)