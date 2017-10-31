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

For downloading images there were 2 option I could take. One would be to use Python requests and the other would be to use xargs in a terminal. I used xargs as after testing I was able to successfully download more images with it. Unfortunately even with 4000 odd URL's for images of receipts I only managed to download just over 2000 of them. This was due to a large number of them no longer being available or otherwise failing to respond to my request. I expect this number to go down when I go over them so an extra source may be necessary when it comes to training the neural network I will be making. 

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

## Making a dataset

Making the dataset was the case of taking in every image I downloaded and had not removed after checking over them in addition to any image I had added (I added around 300 images). The Python script makeData takes in the images and make some pseudo random edits to them and saves the original and the edits to PNG files. The output is the images in folders. All the receipt images are in a folder called "receipt" and the others are in a folder called "notReceipt". The Python script works but is not perfect. For the images I had (5429) it took about 10 minutes to run and there is no error checking for input images. It is expected the directory containing the input images only contains images. I decided not to make the edits to improve the script because I would only run through the script once, so the extra time spent improving the script would be higher than just running through it as it is.

In total I inputted 5429 images of which 2008 were receipts and 3421 were other. The output contained 12048 images of receipts and 20526 of other images coming to a total of 32574 images. I will need to balance this before training.

~~~Python
import numpy as np
import os
from PIL import Image
from PIL import ImageFilter
from random import uniform, randint
~~~

To access, edit and save the images I used the packages listed above.

~~~Python
# returns a image which has been randomly cropped
def imageCrop(CurrentImage):
    width, height = CurrentImage.size
    return CurrentImage.crop((width/uniform(8, 15), height/uniform(8, 15), (width - width/uniform(8, 15)), (height - height/uniform(8, 15))))

# returns the input image randomly rotated
def imagerotate(CurrentImage):
    return CurrentImage.rotate(randint(1, 359))

# returns the input image randomly blured
def imageGaussianBlur(CurrentImage):
    return CurrentImage.filter(ImageFilter.GaussianBlur(uniform(0.5, 1.7)))

# returns the input image randomly sharpened
def imageUnsharpMask(CurrentImage):
    return CurrentImage.filter(ImageFilter.UnsharpMask(uniform(0.5, 1.7), randint(1, 500), randint(1, 3)))

# loads in a image and edits it. One image will output six images
def loadImages(filePath, saveLocation, i, j):
	for file in os.listdir(filePath):
		newImage = Image.open(filePath + file).convert("L")
		imageDone(newImage, saveLocation, i, 1)
		imageDone(imageCrop(newImage), saveLocation, i, 2)
		imageDone(imagerotate(newImage), saveLocation, i, 3)
		imageDone(imagerotate(newImage), saveLocation, i, 4)
		imageDone(imageGaussianBlur(newImage), saveLocation, i, 5)
		imageDone(imageUnsharpMask(newImage), saveLocation, i, 6)

		i += 1
		j += 6

		if i % 500 == 0:
			print("Images saved:", j)
	return i, j
~~~

This section of script controls the editing of the images. It is given a directory and will go through the content. Each image will be edited and output one in black and white, one cropped, two rotated, one blurred and one sharpened which causes noise. Each image is then sent to be saved (not included in this section). With all the edits except making each image black and white are pseudo random within a given range.

~~~ Python
def imageDone(CurrentImage, saveLocation, i, num):
	CurrentImage = CurrentImage.resize((128, 128))
	CurrentImage = np.array(CurrentImage)
	CurrentImage = Image.fromarray(CurrentImage)
	CurrentImage.save(saveLocation + str(i) + "_" + str(num) + ".png", "PNG")
~~~

Once edited the image is saved. This takes the image, converts it to a 128 by 128 pixel image (with no crop) then saves it as a PNG image to the given path.

## balancing data

As mentioned with making the dataset it is very unbalanced. To fix this balanceData.py takes in every file and what category it is under and adds them all to one numpy array which is saved. Along the way this is balanced to which ever category has the smallest length.

~~~Python
import numpy as np
import os
import random
~~~

~~~Python
# Returnes an array for image file paths and image type
def addItem(filePath, type):
	data = []
	for file in os.listdir(filePath):
		data.append([filePath + file, type])
	return data


# folders containing images
receipt = "K:/notReceipt/processed/receipt/"
notReceipt = "K:/notReceipt/processed/notReceipt/"

receiptData = addItem(receipt, 'receipt')
notReceiptData = addItem(notReceipt, 'notReceipt')

random.shuffle(receiptData)
random.shuffle(notReceiptData)
~~~

This section reads in each file and adds them to corresponding arrays. The arrays are shuffled at this point. This is not required but as I did not need the images in sequence and will be cutting off a section of the array shuffling the array will mean most of the original images will still be used.

~~~Python
# ensures receipts and notReceipts are balanced
if len(receiptData) > len(notReceiptData):
	maxLengh = len(receiptData)
else:
	maxLengh = len(notReceiptData)

print(len(receiptData), len(notReceiptData))

receiptData = receiptData[:maxLengh]
notReceiptData = notReceiptData[:maxLengh]

print(len(receiptData), len(notReceiptData))

# joins seperate arrays and saves it as a numpy array
data = np.concatenate((receiptData, notReceiptData))
random.shuffle(data)
print(len(data))
np.save('notReceiptData.npy', data)
~~~

Finally, the longest array is shortened to the length of the shortest array and both arrays are joined together. The arrays are reshuffled again and then saved to file.
