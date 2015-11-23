from random import random

link_factor = 2
total_pages = 20
usedlinks = []
html_begin = """
<html>
	<title> PAGE </title>
	<body>
"""

uri_template = """<a href="http://localhost/%d.html"> %d </a> </br>"""

html_end = """
	</body>
</html>
"""

site = {}

for page in range(0, total_pages):
	site[page] = []

for i in xrange( link_factor*total_pages):
	page = int(random()*1000) % total_pages
	link_to = int(random()*1000) % total_pages
	if link_to not in usedlinks:
                site[page].append(link_to)
                usedlinks.append(link_to)


for page in site:
	f_pg = open("%s.html" %(page), "w")
	f_content = html_begin + "\n".join([uri_template %(lnk, lnk) for lnk in site[page]]) + html_end
	f_pg.write(f_content)
	f_pg.close()
	print page, site[page]
	
