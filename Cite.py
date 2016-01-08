"""
Use with Python 3.4

This program uses Tsorter by Terrill Dent, licensed under the MIT licence: http://terrill.ca/sorting/tsorter/LICENSE

Requires also lxml

This is a very early draft of a program. Use more as food for though rather than as a production tool.
"""
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.embed import file_html
from bokeh.resources import CDN
import collections
from sys import argv
from gexf import *
from itertools import combinations
import numpy as np
#import matplotlib.pyplot as plt
#from wordcloud import WordCloud, STOPWORDS
#import image

script, filename = argv

plotyears = []
cr = []
authors = []
journals = []
keywords = []
keywordset = []

records = 0
citrefcounter = 0
authorcounter = 0
journalcounter = 0
keywordcounter = 0

#indexbody = [] Used to write everything to the index file. Memory overload.
authorbody = []
journalbody = []
keywordbody = []

wclist = []

indexbodydict= {}
citrefdictionary = {}
citationnetworkdict = {}

gexf = Gexf("Keyword Co-occurrence Network", "File:" + filename + ".")
graph = gexf.addGraph("directed", "static", "Web of Science Keyword network")



# Open up the Web of Science source data as a tsv file.
with open(filename,'r') as tsv: # change file-name here
    next(tsv) # This skips the first line in the file, which contains the TSV headers
    WoSdata = [line.strip().split('\t') for line in tsv] #reads everything as a list

# This loop parses, redefines and writes the values selecte to 'index.html'
for W in WoSdata:
    PT = W[0] #Publication Type
    AU = W[1] # Authors
    BA = W[2] # ?
    BE = W[3] # Editors of Proceedings
    GP = W[4] # ?
    AF = W[5] # Authors Full
    BF = W[6] # ?
    CA = W[7] # Group Authors
    TI = W[8] # Title
    SO = W[9] # Source (Journal title, full)
    SE = W[10] #Book Series title
    BS = W[11] # ?
    LA = W[12] # Language
    DT = W[13] # Document Type
    CT = W[14] # Conference Title
    CY = W[15] # Conference Date
    CL = W[16] # Conference Location
    SP = W[17] # Conference Sponsors
    HO = W[18] # Conference Host
    DE = W[19] # Original Keywords
    ID = W[20] # New Keywords by ISI (keywords plus)
    AB = W[21] # Abstract
    C1 = W[22] # Research Addresses: Note [] in fields.
    RP = W[23] # Reprint Address
    EM = W[24] # E-mail (Semi-colon separated)
    RI = W[25] # Researcher ID
    OI = W[26] # ?
    FU = W[27] # Funding agency and grant number
    FX = W[28] # Funding text
    CR = W[29] # Cited references (Semi-colon separated)
    NR = int(W[30]) # Cited reference count (Numerical value)
    TC = int(W[31]) # Times cited (Numerical value)
    Z9 = int(W[32]) # Total times Cited
    U1 = int(W[33]) # ?
    U2 = int(W[34]) # ?
    PU = W[35] # Publisher
    PI = W[36] # Publisher city
    PA = W[37] # Publisher Address
    SN = W[38] # ISSN (String value)
    EI = W[39] # ?
    BN = W[40] # ISBN
    J9 = W[41] # 29 Character Journal Abbreviation
    JI = W[42] # ISO Journal Title Abbreviation
    PD = W[43] # Publication date (mixed string and possible integer value)
    PY = int(W[44]) # Publication Year (Could also be parsed with date module)
    VL = W[45] # Volume (could also be parsed as an integer, but no really useful)
    IS = W[46] # Issue (contains both numerical values and hyphenations)
    PN = W[47] # Part Number
    SU = W[48] # Supplement (number)
    SI = W[49] # Special Issue
    MA = W[50] # ?
    BP = W[51] # Beginning page
    EP = W[52] # End page
    AR = W[53] # Article number of APS journals
    DI = W[54] # DOI Number
    D2 = W[55] # ?
    PG = int(W[56]) # Number of Pages
    WC = W[57] # Research Field
    SC = W[58] # Science Categories?
    GA = W[59] # IDS number, ISI original
    UT = W[60] # WOS ISI unique artile identifier

    #Count records
    if PT:
        records += 1
    else:
        continue

    for category in WC.split('; '):
        wclist.append(category)



    #Append the content of the table
    #Problem: This writes too many records! Limit to 500 or something
    indexbodydict.update({'<tr>\n<td>' + AU + '<br><a href="http://dx.doi.org/'
    + DI + '" target="_blank"><div title="' + AB + '">' + TI + '</div>\n</a></td>'
    + '\n<td>' + SO + '</td>\n <td>' + str(PY) + '</td><td>'
    + str(TC) + '</td>\n</tr>\n': TC})

    """ Old function to add everything to index file. Too memory heavy.
    indexbody.append('<tr>\n<td>' + AU + '<br><a href="http://dx.doi.org/'
    + DI + '" target="_blank"><div title="' + AB + '">' + TI + '</div>\n</a></td>'
    + '\n<td>' + SO + '</td>\n <td>' + str(PY) + '</td><td>'
    + str(TC) + '</td>\n</tr>\n')
    """

    #Create list of years
    plotyears.append(PY)
    journals.append(SO)

    keywordset.append(DE.split('; '))
    #Loop and split cited references

    citationnetworkdict.update({AU: CR.split('; ')})
    for citref in CR.split('; '):
        #citrefdictionary.update({citref: UT}) # This creates a dictionary for each CR so that UT can be extracted.
        cr.append(citref)
        citrefcounter += 1
    for au in AU.split('; '):
        authors.append(au)

    for keyw in DE.split('; '):
        if len(keyw) < 1:  #remove empty ones
            continue
        else:
            keywords.append(keyw.lower())
            graph.addNode(keyw.lower(), keyw.lower())
#print(citrefdictionary)


#print(wclist)

authorcount = collections.Counter(authors)
for a in authorcount: #count unique authors, not duplicates
    authorcounter += 1
for author, count in authorcount.most_common(500):
    authorbody.append("<tr>\n<td>" + author + "</td>\n<td>" + str(count) + "</td>\n</tr>\n")

journalcount = collections.Counter(journals)
for j in journalcount:
    journalcounter +=1
for journal, count in journalcount.most_common(500):
    journalbody.append("<tr>\n<td>" + journal + "</td>\n<td>" + str(count) + "</td>\n</tr>\n")

keywordcount = collections.Counter(keywords)
for k in keywordcount:
    keywordcounter +=1
for keyword, count in keywordcount.most_common(1000):
    keywordbody.append("<tr>\n<td>" + keyword + "</td>\n<td>" + str(count) + "</td>\n</tr>\n")

wclistcount = collections.Counter(wclist)
for wc, count in wclistcount.most_common(20):
    print(wc + "\t" + str(count))

### Create edges for a keyword cooccurrence network:

edgelist = []

for k in keywordset:
    cooccurrence = list(combinations(k, 2))
    for c in cooccurrence:
        edgelist.append(c)

for enumer, edge in enumerate(edgelist):
    #print(enumer, edge[0].lower(), edge[1].lower())
    graph.addEdge(enumer, edge[0].lower(), edge[1].lower())

gexf_file = open(filename + "Keywords.gexf", "wb")
gexf.write(gexf_file)
###

#### Create graphviz (experimental)
"""
from graphviz import Digraph

u = Digraph('unix', filename='testargraphviz.gv')
u.body.append('size="6,6"')
u.node_attr.update(color='lightblue2', style='filled')

testlist = [('katt', 'fax'), ('kille', 'tjej')]

edgetoplist = collections.Counter(edgelist)
#print(edgetoplist)
for n in edgetoplist.most_common(100):
    print(n)

for edge, value in edgetoplist.most_common(100):
    edge1 = edge[0].lower()
    edge2 = edge[1].lower()
    u.edge(edge1, edge2)

u.view()
"""

### Create nodes and edges for Citation network.
gexf = Gexf("Citation Network", "File:" + filename + ".")
graph = gexf.addGraph("directed", "static", "Web of Science Citation network")

numberofedges = 0
for key, value in citationnetworkdict.items():
    graph.addNode(key, key)

    for v in value:
        graph.addNode(v,v)
        #print(str(numberofedges) + "***" + key + "***" + v)
        graph.addEdge(str(numberofedges), key, v)
        numberofedges += 1

gexf_file = open(filename + "Citations.gexf", "wb")
gexf.write(gexf_file)
    #print("***" + key, value) for v in value
    #for enumer, v in value:
    #    print(enumer, v)




### Create graph with Bokeh
counter = collections.Counter(plotyears) #count them
output_file("years.html", title="Citepy - Yearly distribution of records")

years = []
val   = []
yearvaldict = {}

for number in sorted(counter): #This puts years and values
    years.append(number)
    value = counter[number]
    val.append(value)
    yearvaldict[number] = [value]

for key, value in yearvaldict.items():
    print(key, value)
# Convert your data into a panda DataFrame format
data=pd.DataFrame({'year':years, 'value':val})

# Create a new column (yearDate) equal to the year Column but with a datetime format
data['yearDate']=pd.to_datetime(data['year'],format='%Y')

# Create a line graph with datetime x axis and use datetime column(yearDate) for this axis
p = figure(width=600, height=150, x_axis_type="datetime") #, tools="reset, save, pan, wheel_zoom")
p.logo = None
p.toolbar_location = None #"right"
p.line(x=data['yearDate'],y=data['value'], color="#B7ADCF", line_width=2)
#show(p)
bokehhtml = file_html(p, CDN, "Yearly Distribution of Records")
save(p)

#htmlfile.write(html)
### /Create graph with Bokeh.

"""
#Create wordcloud of keywords
# Stopwords, just add more if needed.
stopwords = STOPWORDS
stopwords.add("et")
stopwords.add("will")
stopwords.add("al")
stopwords.add("also")


# Generating wordcloud (change size)
wordcloud = WordCloud(
        background_color="white",
        max_words=500,
        stopwords=STOPWORDS,
        width=3000,
        height=1500
        )
wordcloud.generate(str(keywords))

# Generating the image and showing it.
plt.imshow(wordcloud)
plt.axis("off")
print('Saving Wordcloud as: ' + filename + '.png')
plt.savefig(filename + '.png') # change to .svg, .pdf etc. for other outputs.
##plt.show()

"""


################ BEGIN HTML RENDERING ###################################
### This defines the header, opens 'index.html' and writes the header.
htmlfile = open('index.html','w')
crfile = open('cr.html','w')
authorfile = open('authors.html','w')
journalfile = open('journals.html', 'w')
keywordfile = open('keywords.html', 'w')

header = '''
<!DOCTYPE html>
<html>
<head>
<link href="style.css" rel="stylesheet">
</head>

<script>
function init() {
    var sorter = tsorter.create('result_table');
}

window.onload = init;
</script>
<h1>Results for <em>''' + filename + ''' </em></h1>
<!-- <br> <a href="''' + filename + '''.png"><img src="''' + filename + '''.png" width="100" /></a> -->
<p>

''' + bokehhtml + '''

<a href="index.html">Records</a>: ''' + str(records) + '''
<a href="authors.html">Authors</a>: ''' + str(authorcounter) + '''
<a href="journals.html">Journals</a>: ''' + str(journalcounter) + '''
<a href="cr.html">Cited References</a>: ''' + str(citrefcounter) + '''
<a href="keywords.html">Original Keywords</a>: ''' + str(keywordcounter) + '''
<br><a href="years.html">Yearly output (graph)</a> |
<a href="''' + filename + '''Keywords.gexf">Keyword Co-occurrence Network (.gexf)</a> |
<a href="''' + filename + '''Citations.gexf">Citation Network (Authors, Cited references) (.gexf)</a> |
<!-- <a href="''' + filename + '''.png">Wordcloud of Keywords</a> -->
</p>
'''

indexbodytop = """
<table id="result_table" class="sortable">
    <thead>
        <tr>
            <th>Author / Title</th>
            <th>Journal</th>
            <th data-tsorter="numeric">Year</th>
            <th data-tsorter="numeric">Citations</th>
        </tr>
    </thead>
    <tbody>
"""

crbodytop = """
<table id="result_table" class="sortable">
    <thead>
        <tr>
            <th>Author</th>
            <th data-tsorter="numeric">Year</th>
            <th>Journal</th>
            <th>Volume</th>
            <th>Start page</th>
            <th>DOI</th>
            <th data-tsorter="numeric">Cited in dataset</th>
        </tr>
    </thead>
    <tbody>
"""


authorbodytop = """
<table id="result_table" class="sortable">
    <thead>
        <tr>
            <th>Author</th>
            <th data-tsorter="numeric">Authorship in dataset</th>
        </tr>
    </thead>
    <tbody>
"""

journalbodytop = """
<table id="result_table" class="sortable">
    <thead>
        <tr>
            <th>Journals</th>
            <th data-tsorter="numeric">Records in dataset</th>
        </tr>
    </thead>
    <tbody>
"""

keywordbodytop = """
<table id="result_table" class="sortable">
    <thead>
        <tr>
            <th>Keyword</th>
            <th data-tsorter="numeric">Occurrences in dataset</th>
        </tr>
    </thead>
    <tbody>
"""

htmlfile.write(header + indexbodytop)
crfile.write(header + crbodytop)
authorfile.write(header + authorbodytop)
journalfile.write(header + journalbodytop)
keywordfile.write(header + keywordbodytop)

#Write the content of the main table
#Note, arranged by most cited with the 'most_common' variable
for record in dict(collections.Counter(indexbodydict).most_common(500)):
    htmlfile.write(record)

""" This one used to print everything as index. Makes computer run out of memory.
for i in indexbody:
    htmlfile.write(i)
"""

for a in authorbody:
    authorfile.write(a)

for j in journalbody:
    journalfile.write(j)

for k in keywordbody:
    keywordfile.write(k)


# Create Cited referece (cr.html) table content.
crcount = collections.Counter(cr) #Count them
for citedreference, count in crcount.most_common(500):
    crfile.write("<tr>\n")
    #if len(citedreference) < 1:   #Needed because empty values screws the sorting up.
    #    crfile.write("<td>Unknown</td>")
    #else:
    crsplit = (citedreference.split(', '))
    try:
        if len(crsplit[0]) > 1:
            crfile.write("<td>" + crsplit[0] + "</td>")
        else:
            crfile.write("<td>Unknown</td>")
    except IndexError:
        crfile.write("<td>" + "N/A" + "</td>")
    try:
        crfile.write("<td>" + crsplit[1] + "</td>")
    except IndexError:
        crfile.write("<td>" + "N/A" + "</td>")
    try:
        crfile.write("<td>" + crsplit[2] + "</td>")
    except IndexError:
        crfile.write("<td>" + "N/A" + "</td>")
    try:
        if crsplit[3].startswith("DOI"): #Very rarely the data starts wit DOI DOI. Another elif-statement may prevent this.
            crfile.write('<td>N/A</td><td>N/A</td><td><a href="http://dx.doi.org/' + crsplit[3][4:] + '">' + crsplit[3][4:] + '</td>\n<td>' + str(count) + '</td></tr>\n')
            continue
        else:
            crfile.write("<td>" + crsplit[3] + "</td>")
    except IndexError:
        crfile.write("<td>" + "N/A" + "</td>")
    try:
        if crsplit[4].startswith("DOI"):
            crfile.write('<td>N/A</td><td><a href="http://dx.doi.org/' + crsplit[4][4:] + '">' + crsplit[4][4:] + '</td>\n<td>' + str(count) + '</td></tr>\n')
            continue
        else:
            crfile.write("<td>" + crsplit[4] + "</td>")
    except IndexError:
       crfile.write("<td>" + "N/A" + "</td>")
    try:
       crfile.write('<td><a href="http://dx.doi.org/' + crsplit[5][4:] + '">' + crsplit[5][4:] + '</td>')
    except IndexError:
       crfile.write("<td>" + "N/A" + "</td>")
    crfile.write("<td>" + str(count) + "</td>")
    crfile.write("</tr>\n")




### Print the footer and close the files
footer = """
    </tbody>
</table>

<script src="tsorter.min.js" type="text/javascript"></script>

</body>
</html>
"""
#Write and save m files
htmlfile.write(footer)
htmlfile.close()
crfile.write(footer)
crfile.close()
authorfile.write(footer)
authorfile.close()
journalfile.write(footer)
journalfile.close()
keywordfile.write(footer)
keywordfile.close()



### Boot up web server and open in browser
import webbrowser
#webbrowser.open('http://localhost:8000/index.html')
import http.server
import socketserver

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print("Serving at port", PORT)
httpd.serve_forever()
