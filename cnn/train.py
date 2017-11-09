import numpy as np
from PIL import Image
# import pickle # use this to load and save model


# returns arrays for training and testing data
def getData(inputFile):
	data = np.load(inputFile)
	test = data[::4]
	train = np.concatenate([data[1::4], data[2::4], data[3::4]])
	# print('Length of training data: ', len(train))
	# print('Length of testing data: ', len(test))
	return train, test

# Convolutional Layer - This will take in a image an an array, size of filter ((int, int)), stride (int), padding (int), filterSize (int) and filters (array - optional) and bias (array - optional)
# Output array, filters (array), bias (array)
def convolution(image, filterSize, stride, padding, filterLayers, filters=None, bias=None):
	if (((image.shape[0] - filterSize[0] + 2 * padding) / stride) + 1).is_integer():  # checks output is an int
		if (((image.shape[1] - filterSize[1] + 2 * padding) / stride) + 1).is_integer():  # checks output is an int
			outshape = np.zeros([int((((image.shape[0] - filterSize[0] + 2 * padding) / stride) + 1)), int((((image.shape[1] - filterSize[1] + 2 * padding) / stride) + 1)), filterLayers], dtype=int)  # creats the activation map (empty)
			image = np.pad(image, ((padding,padding), (padding,padding), (0,0)), mode='constant')  # adds padding of 0's arround image
		else:
			print("Convolution is not possible. Try a different stride or padding")
			return
	else:
		print("Convolution is not possible. Try a different stride or padding")
		return

	# Creats filters if they dont already exist
	if filters == None:
		filters = []
		for i in range(filterLayers):
			filters.append(np.zeros([filterSize[0], filterSize[1], image.shape[2]], dtype=int))

	# Creats bias if they dont already exist
	if bias == None:
		bias = []
		for i in range(filterLayers):
			newBias = np.zeros([1, 1, 1], dtype=int)
			newBias[0, 0, 0] = 0
			bias.append(newBias)

	# Goes over each section of the input image by size specified by the filter and sums up element wise matrix multiplication to the output
	for i in range(outshape.shape[2]):  # number of filters
		filterArray = filters[i]
		for j in range(0, outshape.shape[1]):  # height of activation map
			for k in range(0, outshape.shape[0]):  # width of activation map
				outshape[k, j, i] = np.sum(image[k*stride:filterArray.shape[0] + k*stride, j*stride:filterArray.shape[1] + j*stride, :] * filterArray[:, :, :]) + bias[i]
		return outshape, filters, bias # retult, filiters and bias returned

# This is test data - delete this once finnished makeing CNN
def exampleTestData():
	test1 = np.array([[1, 0, 2, 1, 0],
						[1, 2, 1, 1, 1],
						[0, 2, 2, 2, 1],
						[1, 1, 1, 1, 1],
						[2, 2, 1, 2, 1]])

	test2 = np.array([[2, 1, 0, 2, 2],
						[0, 0, 1, 0, 1],
						[2, 2, 0, 2, 0],
						[1, 1, 0, 2, 0],
						[2, 1, 0, 2, 1]])

	test3 = np.array([[2, 1, 1, 0, 0],
						[0, 1, 1, 0, 2],
						[2, 0, 0, 2, 2],
						[0, 1, 1, 1, 0],
						[2, 2, 1, 2, 1]])

	testArray = np.zeros([5, 5, 3], dtype=int)

	testArray[:, :, 0] = test1
	testArray[:, :, 1] = test2
	testArray[:, :, 2] = test3

	w0Test1 = np.array([[1, 1, -1],
						[0, 0, 0],
						[-1, 1, 0]])

	w0Test2 = np.array([[-1, 0, 1],
						[-1, 0, 1],
						[-1, 0, -1]])

	w0Test3 = np.array([[1, 0, -1],
						[-1, 0, 1],
						[1, 1, 1]])

	w0 = np.zeros([3, 3, 3], dtype=int)

	w0[:, :, 0] = w0Test1
	w0[:, :, 1] = w0Test2
	w0[:, :, 2] = w0Test3

	w1Test1 = np.array([[-1, 1, 1],
						[0, 1, -1],
						[1, 1, 1]])

	w1Test2 = np.array([[0, 1, -1],
						[1, 0, 1],
						[0, -1, 1]])

	w1Test3 = np.array([[0, 1, 1],
						[1, -1, 0],
						[0, -1, 0]])

	w1 = np.zeros([3, 3, 3], dtype=int)

	w1[:, :, 0] = w1Test1
	w1[:, :, 1] = w1Test2
	w1[:, :, 2] = w1Test3

	testFilters = [w0, w1]

	b1 = np.zeros([1, 1, 1], dtype=int)
	b1[0, 0, 0] = 1
	b2 = np.zeros([1, 1, 1], dtype=int)
	b2[0, 0, 0] = 0

	biasTest = [b1, b2]

	convolution(testArray, (3, 3), 2, 1, 2, testFilters, biasTest)


exampleTestData()


trainData, testData = getData("notReceiptData.npy")

# np.set_printoptions(threshold=np.nan)

# more test data (this uses a real image)
newImage = Image.open(trainData[0][0])
newImage = np.array(newImage)  # pass this into convolution as image
newImage = np.reshape(newImage, (newImage.shape[0], newImage.shape[1], 1))
outputData, conFilters, conBias = convolution(newImage, (64, 64), 1, 1, 8)