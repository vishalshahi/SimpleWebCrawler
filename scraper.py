import sys
import os
import re
import httplib
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup
import shortuuid

#keep the current working directory
rootdir = os.getcwd()

#regex to check validity of url
regex = re.compile(
	r'^(?:http|ftp)s?://' 
	r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
	r'localhost|' 
	r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
	r'(?::\d+)?'
	r'(?:/?|[/?]\S+)$', re.IGNORECASE)

#Remove whitespaces and other characters from url
def getTrimmedUrl(url):
	return url.replace("http:","").replace(" ","").replace("/", "")


def isValidUrl(url):
	if regex.match(url) is not None:
		return True
	return False

#parse the web page to extract the links
def getLinks(dr):
	pagesource=urllib2.urlopen(dr)
	s=pagesource.read()
	soup=BeautifulSoup(s,"lxml")
	links=soup.findAll('a',href=True)
	return links

#create a directory and save the contents of the link in a text file 
def saveContent(page ,s ,processed):
#	mpage = getTrimmedUrl(page)
	mpage = shortuuid.uuid(name=page)  #creates unique id from url
	if not os.path.exists(mpage):
		os.makedirs(mpage)
		old = os.getcwd()
		#change the current working directory before creating the file
		os.chdir(old + '/' + mpage)
		with open(mpage+'.txt','w') as f:
			f.write(s)
		#restore the CWD 
		os.chdir(old)
		#Add the page to the processed queue
		processed.append(page)

def crawler(SeedUrl):
	tocrawl=[SeedUrl,'$']   # Queue to store the links separated by special character '$' indicating folder hierarchy
	crawled=[]		# No. of links crawled
	processed=[]		# helper queue to create a directory structure
	topop = True		# topop : False -> indicates a web page with no links
	while tocrawl:
#		print processed
		if topop:
			page=tocrawl.pop(0)

		if not page == '$':

			print 'Crawled:'+page
			pagesource=urllib2.urlopen(page)
			s=pagesource.read()
			saveContent(page,s,processed)      #saves the content of the web page to a text file 
			soup=BeautifulSoup(s,"lxml")
			links=soup.findAll('a',href=True)  # Extracts the anchor tags
			#store all the links in this page to the queue        
			if page not in crawled:
				for l in links:
					if isValidUrl(l['href']):
						if l['href'] not in tocrawl and l['href'] not in crawled and not page == l['href']:
							tocrawl.append(l['href'])
				tocrawl.append('$')     # add special character at the end , which represents some sort of directory level
				crawled.append(page)
#				print tocrawl
		else:
			# change the cuurent working directory as per the directory structure
			# The fisrt element in the processed queue is now the CWD directory
			if processed:
				dr = processed.pop(0)
				links = getLinks(dr)
				if links:
					topop = True
#					tr = getTrimmedUrl(dr) # convert url to folder name and search fo the dirctory
					tr = shortuuid.uuid(dr) #creates unique id from url
					for root, subdirs, files in os.walk(rootdir):  #traverse the directories from base directory
						if tr in subdirs:
							os.chdir( os.path.abspath(os.path.join(root,tr)))
				else:
					# No links indicates a dead web page
					topop = False
			else:
				topop = True
 	
	return crawled      # return the list of urls crawled

def main():
	try:
		crawler(sys.argv[1])
	except urllib2.HTTPError:
		print ('Could not connect to url')

if __name__ == "__main__":
	main()
