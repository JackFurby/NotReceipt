import numpy as np
import os
from PIL import Image
from PIL import ImageFilter
from random import uniform, randint

# resizes the image and saves them as PNG images
def imageDone(CurrentImage, saveLocation, i, num):
	CurrentImage = CurrentImage.resize((128, 128))
	CurrentImage = np.array(CurrentImage)
	CurrentImage = Image.fromarray(CurrentImage)
	CurrentImage.save(saveLocation + str(i) + "_" + str(num) + ".png", "PNG")

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

# folders there the images are found and saved
receiptFrom = "K:/notReceipt/original/receipt/"
notReceiptFrom = "K:/notReceipt/original/notReceipt/"
receiptTo = "K:/notReceipt/processed/receipt/"
notReceiptTo = "K:/notReceipt/processed/notReceipt/"

# totals for images
i = 0
j = 0

# creats directories to save images to if they dont exist
if not os.path.exists(receiptTo):
	os.makedirs(receiptTo)
if not os.path.exists(notReceiptTo):
	os.makedirs(notReceiptTo)

# creats images of receipts
i , j = loadImages(receiptFrom, receiptTo, i, j)
print("\n\n--------------\n\n" + "Total input receipt images:", i)
print("Total output receipt images:", j, "\n\n--------------\n\n")

# creats images of none receipts
i, j = loadImages(notReceiptFrom, notReceiptTo, i, j)
print("\n\n--------------\n\n" + "Total input none receipt images:", i)
print("Total output none receipt images:", j, "\n\n--------------")

print("\n\n--------------\n\n" + "Total input images:", i)
print("Total output images:", j, "\n\n--------------\n\n")
