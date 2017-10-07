from lxml import html
import requests
import csv

# array to store all image URL's
allImages = []

# gets URL of each image on each page on expressexpense.com/view-receipts.php
for i in range(86):
    pageNum = i + 1
    page = requests.get('https://expressexpense.com/view-receipts.php?page=%s' % pageNum)
    tree = html.fromstring(page.content)
    images = tree.xpath('//div[@class="record"]//a/@data-featherlight')
    allImages += images

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
