from lxml import html
import requests
import csv

# array to store all image URL's
allImages = []

# gets URL of each image on each page on www.image-net.org
# n06263609 = printed media, n14974264 = paper, n06793231 = sign, n04152593 = screen
searchTerms = ['n06263609', 'n14974264', 'n06793231', 'n04152593']

for pageSearch in range(len(searchTerms)):
    page = requests.get('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=%s' % searchTerms[pageSearch])
    tree = html.fromstring(page.content)
    images = tree.xpath('//html//body//*/text()')
    allImages += images[0].splitlines()

# writes CSV file with image URL (separated by row)
csvfile = open('notReceipt.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvfile, delimiter=",")
imageNum = 1
for row in allImages:
    writer.writerow([row])
    imageNum += 1
csvfile.close()
