import numpy as np
from PIL import Image
#from sklearn.utils.extmath import softmax
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
			outshape = np.zeros([int((((image.shape[0] - filterSize[0] + 2 * padding) / stride) + 1)), int((((image.shape[1] - filterSize[1] + 2 * padding) / stride) + 1)), filterLayers], dtype=np.float64)  # creats the activation map (empty)
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
			filters.append(np.random.rand(filterSize[0], filterSize[1], image.shape[2]))

	# Creats bias if they dont already exist
	if bias == None:
		bias = []
		for i in range(filterLayers):
			bias.append(np.random.rand(1, 1, 1))

	# Goes over each section of the input image by size specified by the filter and sums up element wise matrix multiplication to the output
	for i in range(outshape.shape[2]):  # number of filters
		filterArray = filters[i]
		for j in range(0, outshape.shape[1]):  # height of activation map
			for k in range(0, outshape.shape[0]):  # width of activation map
				outshape[k, j, i] = np.sum(image[k*stride:filterArray.shape[0] + k*stride, j*stride:filterArray.shape[1] + j*stride, :] * filterArray[:, :, :]) + bias[i]
	return outshape, filters, bias  # result, filters and bias returned


# performs max pooling on a input numpy array. Output will just be a numpy array with max pooling applied
def maxPooling(image, filterSize, stride):
	if (((image.shape[0] - filterSize[0]) / stride) + 1).is_integer():  # checks output is an int
		if (((image.shape[1] - filterSize[1]) / stride) + 1).is_integer():  # checks output is an int
			outshape = np.ones([int(((image.shape[0] - filterSize[0]) / stride + 1)), int(((image.shape[1] - filterSize[1]) / stride + 1)), image.shape[2]], dtype=np.float64)  # creats the output array
		else:
			print("Pooling is not possible. Try a different stride or filter size")
			return
	else:
		print("Pooling is not possible. Try a different stride or filter size")
		return

	for i in range(outshape.shape[2]):  # number of layers
		for j in range(0, outshape.shape[1]):  # height of output array
			for k in range(0, outshape.shape[0]):  # width of output array
				outshape[k, j, i] = np.amax(image[k*stride:k*stride + filterSize[0], j*stride:j*stride + filterSize[1], :])
	return outshape


# performs ReLu on a given numpy array
def relu(image):
	return image.clip(min=0)


# takes in inputArray and expected result, returns predictions and error
def softmax(inputArray):
	#inputArray.astype(np.float64)
	inputArray -= np.max(inputArray)
	output = np.exp(inputArray) / np.sum(np.exp(inputArray))
	return output


def error(input, expected):
	error = np.sum((0.5)*(expected-input)**2)
	return error

def Backpropagation(network, error):
	pass


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

	testArray = np.zeros([5, 5, 3], dtype=np.float64)

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

	w0 = np.zeros([3, 3, 3], dtype=np.float64)

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

	w1 = np.zeros([3, 3, 3], dtype=np.float64)

	w1[:, :, 0] = w1Test1
	w1[:, :, 1] = w1Test2
	w1[:, :, 2] = w1Test3

	testFilters = [w0, w1]

	b1 = np.zeros([1, 1, 1], dtype=np.float64)
	b1[0, 0, 0] = 1
	b2 = np.zeros([1, 1, 1], dtype=np.float64)
	b2[0, 0, 0] = 0

	biasTest = [b1, b2]

	Flatw1 = np.array([[-1, 1, 1],
						[0, 1, -1],
						[1, 1, 1]])

	Flatw2 = np.array([[0, 1, -1],
						[1, 0, 1],
						[0, -1, 1]])

	Flatw3 = np.array([[1, 0, 1],
						[1, 0, -1],
						[1, 0, 0]])

	Flatw4 = np.array([[1, 1, 1],
						[0, 1, -1],
						[0, -1, 1]])

	Flatw5 = np.array([[0, 0, 0],
						[1, 1, 1],
						[-1, -1, -1]])

	Flatw6 = np.array([[0, 0, 1],
						[1, -1, 1],
						[1, 1, 0]])

	Flatw7 = np.array([[0, 0, -1],
						[1, 1, 1],
						[1, 0, -1]])

	Flatw8 = np.array([[0, -1, 0],
						[-1, 0, -1],
						[0, -1, 0]])

	Flatw9 = np.array([[-1, -1, -1],
						[1, -1, -1],
						[1, 1, 1]])

	Flatw10 = np.array([[0, 0, 0],
						[1, 1, 1],
						[0, 0, 0]])

	flatFilterTest = np.zeros([3, 3, 10], dtype=np.float64)

	flatFilterTest[:, :, 0] = Flatw1
	flatFilterTest[:, :, 1] = Flatw2
	flatFilterTest[:, :, 2] = Flatw3
	flatFilterTest[:, :, 3] = Flatw4
	flatFilterTest[:, :, 4] = Flatw5
	flatFilterTest[:, :, 5] = Flatw6
	flatFilterTest[:, :, 6] = Flatw7
	flatFilterTest[:, :, 7] = Flatw8
	flatFilterTest[:, :, 8] = Flatw9
	flatFilterTest[:, :, 9] = Flatw10

	testFlatFilters = [flatFilterTest]

	outputData, conFilters, conBias = convolution(testArray, (3, 3), 2, 1, 2, testFilters, biasTest)
	# print(outputData)
	# print(outputData.shape)
	outputDataPooling = maxPooling(outputData, (2, 2), 1)
	# print(outputDataPooling)
	outputRelu = relu(outputData)
	# print(outputRelu)
	# print(outputRelu.shape)
	outputFlatten, flattenFilters, flattenBias = convolution(outputRelu, (outputRelu.shape[0], outputRelu.shape[1]), 1, 0, 10) # flatten
	outputFlatten2, flattenFilters2, flattenBias2 = convolution(outputRelu, (outputRelu.shape[0], outputRelu.shape[1]), 1, 0, 2) # flatten
	# outputFC, weightsFC, biasFC = fullyConnected(outputFlatten, 2)
	# print(outputFC)
	softmaxResult, softmaxError = softmax(outputFlatten2[0][0], [0, 1])

	# testing for pooling

	testPooling = np.empty([4, 4, 1], dtype=np.float64)

	testPooling[:, :, 0] = np.array([[1, 1, 2, 4],
							[5, 6, 7, 8],
							[3, 2, 1, 0],
							[1, 2, 3, 4]])

	# print(testPooling[:,:,0])

	outputDataPooling = maxPooling(testPooling, (2, 2), 2)

	# print(outputDataPooling[:,:,0])

	outputRelu = relu(outputData)
	# print(outputRelu.shape)
	# print(outputRelu)

	outputFlatten, flattenFilters, flattenBias = convolution(outputRelu, (outputRelu.shape[0], outputRelu.shape[1]), 1, 0, 10)  # flatten
	# print(outputFlatten.shape)
	outputFlatten2, flattenFilters2, flattenBias2 = convolution(outputRelu, (outputRelu.shape[0], outputRelu.shape[1]), 1, 0, 2)  # flatten
	# print(outputFlatten2)
	# outputFC, weightsFC, biasFC = fullyConnected(outputFlatten, 2)
	# print("outputFC:", outputFC)

	outputRelu = relu(outputFlatten2)

	softmaxResult, softmaxError = softmax(outputRelu[0][0], [0, 1])
	print('result:', softmaxResult,  'error:', softmaxError)

#exampleTestData()


def forwardRun(model, currentImage, currentExpect):

	outputData, conFilters, conBias = convolution(currentImage, (5, 5), 1, 1, 8, model[0][0], bias=model[0][1])
	# print(outputData.shape)

	outputDataPooling = maxPooling(outputData, (2, 2), 2)
	# print(outputDataPooling.shape)

	outputReLu = relu(outputDataPooling)
	# print(outputReLu.shape)
	# print(outputReLu)

	outputFlatten, flattenFilters, flattenBias = convolution(outputReLu, (outputReLu.shape[0], outputReLu.shape[1]), 1, 0, 10, model[1][0], bias=model[1][1])  # flatten
	# print(outputFlatten)
	# print(outputFlatten.shape)
	outputFlatten2, flattenFilters2, flattenBias2 = convolution(outputFlatten, (outputFlatten.shape[0], outputFlatten.shape[1]), 1, 0, 2, model[2][0], bias=model[2][1])  # flatten

	# outputFC, weightsFC, biasFC = fullyConnected(outputFlatten, 2)
	# print("outputFC:", outputFC)

	softmaxResult = softmax(outputFlatten2[0][0])
	#softmaxResult = softmax(outputFlatten2[0][0])
	modelError = error(softmaxResult, currentExpect)
	model = [[conFilters, conBias], [flattenFilters, flattenBias], [flattenFilters2, flattenBias2]]

	return softmaxResult, modelError, model


trainData, testData = getData("notReceiptData.npy")

model = [[None, None], [None, None], [None, None]]

# passes image into model and adds result to array
for image in range(len(trainData)):
	newImage = Image.open(trainData[image][0])
	newImageExpected = trainData[image][1]
	if newImageExpected == 'receipt':
		newImageExpected = [1, 0]
	else:
		newImageExpected = [0, 1]
	# newImage = Image.open("/Users/jack/Documents/programming/notReceipt/dataset/test/0_1.png")
	newImage = np.array(newImage)  # pass this into convolution as image
	newImage = np.reshape(newImage, (newImage.shape[0], newImage.shape[1], 1))
	#print(newImage)
	result, modelError, modelNew = forwardRun(model, newImage, newImageExpected)
	model = modelNew
	print('result:', result,  'error:', modelError)
