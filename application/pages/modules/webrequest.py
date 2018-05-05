'''
v1

Python WebRequest
Contains the tools to request elements from a web page

Usable Functions:

request = request elements
csv_request = request and writes the data in a csv


'''

from datetime import datetime
from urllib.request import urlopen, Request #bibliothèque urllib2
from bs4 import BeautifulSoup #bibliothèque BeautifulSoup
import csv
import sys

class WebRequest(object):
	'''Requesting an indefininate number of objects on a website'''
	def __init__(self, url, elements=[]):
		'''Object attributes'''
		self.url = url
		self.elements = elements 

		def soup(web): 
			'''Scrapes the website'''
			url = urlopen(Request(web, headers={'User-Agent': 'Mozilla/5.0'}))
			return BeautifulSoup(url, 'html.parser')
		
		def check(liste):
			"""Input Errors"""
			for i in liste:
				if not isinstance(i, list):
					sys.exit("\nWebRequest| InputError: Elements list should look like [first element as list, second element as list]")
				elif len(i)<2:
					sys.exit("\nWebRequest| InputError: Element should contain the tag and the attributes \nElement should look like ['tag',{{'attribute':'attribute name'}}]")
				elif not isinstance(i[0], str):
					sys.exit("\nWebRequest| ElementError: {} should be the tag as a string \nElement should look like ['tag',{{'attribute':'attribute name'}}]".format(str(i[0])))
				elif not isinstance(i[1], dict):
					sys.exit("\nWebRequest| ElementError: Element should be a dictionnary \nElement should look like ['tag',{{'attribute':'attribute name'}}]")

		check(elements)

		self.page = soup(url)
		self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	def __str__(self):
		return'<WebRequest | Url: {} | Number of Elements: {} | Timestamp: {}>'.format(self.url, self.elnum, self.timestamp)

	def __len__(self):
		return len(self.elements)

	def request(self):
		'''returns the element request
		Searches for the elements in the order given
		'''
		def to_num(string):
			'''Should return floats if the str is a number:

				Worst case string looks like £1 or $5,3 ( n° char = n° num )
				> Which is why len(str_num)/len(string) >= 0.5 and not >
			
				Another hard one is if the string looks like €1,509.15 ( , and . )
				> When we find , or . checks 4 letters later to determine wether to remove it or not

				Unsolved is when you want to get numbers as strings, such as an appartement number (ex: 204b -> will drop the b)
			'''

			'''Catches numbers, commas and points'''
			numbers=['0','1','2','3','4','5','6','7','8','9',',','.']
			str_num = ''

			for letter in string:
				if letter in numbers:
					str_num = str_num + letter

			'''Checking for case n°2'''
			if len(str_num)>4:
				index = 0
				bol = None
				for h in str_num:
					try:
						if h == ',' and str_num[index+4] == '.':
							bol = ','
							index = index + 1
						elif h == '.' and str_num[index+4] == ',':
							bol = '.'
							index = index + 1
						else:
							index = index + 1
					except:
						pass

				if bol == ',' or bol =='.':
					str_num = str_num.replace(bol,'')

			if len(str_num)/len(string)>=0.5:
				return  float(str_num)
			else:
				return string

		'''Trying to get the text (possible for every request except for images)'''
		try:
			parsed = [self.page.find(element[0], attrs= element[1]).text for element in self.elements]
		except:
			parsed = [self.page.find(element[0], attrs= element[1]) for element in self.elements] 

		'''Treatment of every request'''
		final = []
		for el in parsed:
			
			text = None
			try:
				text = to_num(el)

			except:
				text = el

			finally:
				final.append(text)

		return final

	def csv_request(self, output_file):
		'''same as request method but has a csv output in output_file'''
		with open(output_file, 'a', newline='') as csv_file:
			writer = csv.writer(csv_file)
			request = self.request()
			request.append(self.timestamp)
			writer.writerow(request)
		return request


'''
#<!-- EXEMPLES --!>

kraken = 'https://www.kraken.com/charts'
div = ['div', {'class':'val mono', 'name':'last'}, 'value']
span = ['span', {'class':'pairtext'}, 'tag']

btg = 'https://coinmarketcap.com/currencies/bitcoin-gold/'
el1 = ['span',{'class':'text-large2'}, 'value']
el2 = ['small',{'class':'bold hidden-sm hidden-md hidden-lg'}, 'tag']

test = WebRequest(kraken, [div,span])

test.csv_request('final.csv')
'''