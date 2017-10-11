# Dataset

For my AI to function I will need a dataset of receipts. As it will be working with images my dataset will need to include as many images as I can find. At the time of writing I was unable to find an existing dataset and therefore I will be creating my own. The licence for this repository is for the code. Any media I include may follow a different licence.

## getReceipt.py

This script returns a list of URL's to images of Receipts. I found a database of around 4200 receipts available for anyone to use.

~~~Python
from lxml import html
import requests
import csv
~~~

To access this database I made a web scraper which used the packages listed above.

~~~Python
# array to store all image URL's
allImages = []

# gets URL of each image on each page on expressexpense.com/view-receipts.php
for i in range(86):
    pageNum = i + 1
    page = requests.get('https://expressexpense.com/view-receipts.php?page=%s' % pageNum)
    tree = html.fromstring(page.content)
    images = tree.xpath('//div[@class="record"]//a/@data-featherlight')
    allImages += images
~~~

The site holding the images is expressexpense.com. They have 86 pages of images with each page holding 50 images. The images are not all images and some receipts are old or hand written. This is not a problem but to ensure the data is good I will be going over each result in a future script. This part of the script gets the URL of each image and adds it to an array. I expect there is some more optimization I can do but this part of the script will take some time to complete (mostly loading each web page).

~~~Python
# writes CSV file with image URL in format image URL, image name, 1
# image URL = URL of the image
# image name = name of image once downloaded (will rename image in seperate script)
# 1 = image is of a receipt
csvfile = open('receipt.csv', 'w', newline='')
writer = csv.writer(csvfile, delimiter=",")
imageNum = 1
for row in allImages:
    writer.writerow([row, "receipt-" + str(imageNum), "1"])
    imageNum += 1
csvfile.close()
~~~

The final part of this script takes the URL's and writes them to a CSV file. The CSV file is structured with the first column holding the URL, the second holding the name I will give the image once downloaded and the third holding a 1 which will represent being a receipt.

## getOther.py

This script is much the same as getReceipt.py. The differences it has are with the site it is returning the image URL's from (in this case it is www.image-net.org). There are 4 search terms including printed media, paper, sign and screen. each of these return a XML document with the URL's in text format.

~~~ Python
searchTerms = ['n06263609', 'n14974264', 'n06793231', 'n04152593']

for pageSearch in range(len(searchTerms)):
    page = requests.get('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=%s' % searchTerms[pageSearch])
    tree = html.fromstring(page.content)
    images = tree.xpath('//html//body//*/text()')
    allImages += images[0].splitlines()
~~~

This section of code adds all the URL's from each search term to an array.
