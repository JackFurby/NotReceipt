import numpy as np
import os
import random


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
np.random.shuffle(data)
print(len(data))
np.save('notReceiptData.npy', data)
