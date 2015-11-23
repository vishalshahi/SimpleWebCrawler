# SimpleWebCrawler

This is a simple program to crawl the contents of a web page.
This also stores the contents of all the links in this web page
recursively. All the content are organized and stored in 
a directory structure that resembles the original link
structure of the web pages.

Since it generally goes in an infinite loop
over the internet, I have written a script
to generate random web pages that can be 
hosted locally and used for testing this 
application.

STEPS:

1. Run generate.py
2. Host the generated html files over localhost
3. Run scraper.py as-- python scarper.py "http://www.google.com" or "http://localhost/1.html"
