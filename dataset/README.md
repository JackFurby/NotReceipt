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
# writes CSV file with image URL (separated by row)
csvfile = open('receipt.csv', 'w', newline='')
writer = csv.writer(csvfile, delimiter=",")
imageNum = 1
for row in allImages:
    writer.writerow([row])
    imageNum += 1
csvfile.close()
~~~

The final part of this script takes the URL's and writes them to a CSV file. The CSV file is structured with the URLs separated by row.

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

## Downloading images

For downloading images there were 2 option I could take. One would be to use Python requests and the other would be to use xargs in a terminal. I used xargs as after testing I was able to successfully download more images with it. Unfortunately even with 4000 odd URL's for images of receipts I only managed to download just over 2000 of them. This was due to a large number of them no longer being available or otherwise failing to respond to my request. I expect this number to go down when I go over them so an extra source may be necessary when it come to training the neural network I will be making. 

These commands work fine on Unix systems but for Windows they will not run. You can get round this by installing Windows Subsystem for Linux.

~~~ bash
tr -d '\r' < receipt.csv > newReceipt.csv
~~~

This command removes return at the end of each row in the CSV file.

~~~ bash
awk '{ print "\""$0"\""}' newReceipt.csv > newReceipt2.csv
~~~

Here quotations are added to the beginning and end of each URL so no errors are thrown when some characters are present.

~~~ bash
xargs -P24 -n 1 curl -k -O < newReceipt2.csv
~~~

Finally this command downloads the images. It is using parallelization to speed up the process. I also added the '-k' flag which means there are no certificate checks. This was added as a few of the images could not be downloaded due to not having the correct credentials.

The final command will take a while to complete and you should either run the commands from where you want to save the images or set the save location in the command. The first 2 commands will create a new CSV file. Once you have made the last one (newReceipt2.csv) the previous CSV files are not necessary and they can be deleted. The same commands can be run on notReceipt images with modification to path names.
