import sys
import urllib2
from bs4 import BeautifulSoup
import urllib
url = "http://www.slyyc.asia"
soup = BeautifulSoup(urllib.urlopen(url))
f = open("soup.htm", "w")
f.write(str(soup))


