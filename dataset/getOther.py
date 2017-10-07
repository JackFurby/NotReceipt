from lxml import html
import requests
import csv

# array to store all image URL's
allImages = []

# gets URL of each image on https://www.pexels.com
page = requests.get('https://www.pexels.com/search/paper/' )
tree = html.fromstring(page.content)
allImages +=  tree.xpath('//img[@class="photo-item__img"]/@src')

# writes CSV file with image URL in format image URL, image name, 1
# image URL = URL of the image
# image name = name of image once downloaded (will rename image in seperate script)
# 0 = image not of a receipt
csvfile = open('other.csv', 'w', newline='')
writer = csv.writer(csvfile, delimiter=",")
imageNum = 1
for row in allImages:
    writer.writerow([row, "other-" + str(imageNum), "0"])
    imageNum += 1
csvfile.close()
