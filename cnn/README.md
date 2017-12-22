For the CNN I used a guide which can be found here: http://cs231n.github.io/convolutional-networks/. This guide goes over how the CNN works and includes a small bit of numpy code. I won't go into as great detail as my main goal here is to document my code.

# Convolutional Layer

The convolutional layer has the input of an image, filter size, stride, padding, filter layers, filters and bias. The image will be a numpy array and in my case, will be 1 in depth for the first input as I am suing greyscale. My code does work for more layers however. The filter size just defines the width and height of the filter to be used. The stride is how many pixels will be convolving (slide) across the input image. 3 is the max that should be convolving with 1 being the minimum. padding is how many 0's will be added to each layer of the input image. Filter layers defines the depth of the output but will also state how many layers of filters will be used. The final 2 inputs are filters and bias which is where pre-defined filters and biases can be inputted. If these are left blank new filters and biases will be created.

~~~ Python
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
~~~

The first section of the convolution layer will check the inputs. If the width or height (W) minus the filter (F) width or height plus 2 times padding (P) all divided by the stride (S) plus 1 does not equals an int it will not be possible to complete this layer and the script will stop. If all is good however the output numpy array will be created with the values (W−F+2P)/S+1. The output will have a depth of filterLayers and contain values of type int. If any padding was specified it will also be added to the input image at this point.

~~~ Python
if filters == None:
	filters = []
	for i in range(filterLayers):
		filters.append(np.random.rand(filterSize[0], filterSize[1], image.shape[2]))

# Creats bias if they dont already exist
if bias == None:
	bias = []
	for i in range(filterLayers):
		bias.append(np.random.rand(1, 1, 1))
~~~

If filters and / or bias were blank the above code will create them. For the filters it will make some numpy arrays with the width and height of the input filter size with the depth of the input image depth. This will be repeated for the number of filter layers there are and each time the result will be added to the end of an array. The same is repeated for the bias but the numpy array is always 1x1x1.

~~~ Python
for i in range(outshape.shape[2]):  # number of filters
	filterArray = filters[i]
	for j in range(0, outshape.shape[1]):  # height of activation map
		for k in range(0, outshape.shape[0]):  # width of activation map
			outshape[k, j, i] = np.sum(image[k*stride:filterArray.shape[0] + k*stride, j*stride:filterArray.shape[1] + j*stride, :] * filterArray[:, :, :]) + bias[i]
return outshape, filters, bias  # result, filters and bias returned
~~~

Finally, we get onto the convolve section. Here the image is convolved with each time the section of the image being looked at Element-wise multiplication will be applied to the filter with the bias being added on at the end. The result will be summed up and added to the output matrix. Once complete the output, filters and bias will be returned.

# Pooling Layer

The pooling layer takes in an input of a numpy array, filter size and stride. The output will be a numpy array which has the same depth as the input but will often be smaller than the input in terms of width and height. The aim of this layer is to reduce the amount of data we have to work with.  

~~~ Python
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
~~~

The first section of the max pooling function is very similar to the convolutional layer. It will ensure pooling is possible with the inputs by taking the width and height (W) minus the filter width and height (F) all divided by the stride + 1. This makes up the formula (W-F)/S+1. If the result is an integer the output array will be created with the for mentioned results. The depth will be the same as the input array.

~~~ Python
for i in range(outshape.shape[2]):  # number of layers
	for j in range(0, outshape.shape[1]):  # height of output array
		for k in range(0, outshape.shape[0]):  # width of output array
			outshape[k, j, i] = np.amax(image[k*stride:k*stride + filterSize[0], j*stride:j*stride + filterSize[1], :])
return outshape
~~~

Finally, the polling will occur. This will loop over the input array like with convolution but this time the amax function will be applied within numpy. This will look at a given array and return the highest value. This value will be added to the output. Once complete the output array will be returned.

# ReLu layer

The ReLu layer will take in an input of a numpy array and return an array of the same size but with all values less than 0 replaced with 0.  

~~~ Python
def relu(image):
	return image.clip(min=0)
~~~

# Softmax layer

The softmax layer takes in an array which has the shape 1 by the number of possible classifications of the network. np.max() is performed to reduce one of the classifications to 0 and the other to the difference. This was done as getting the exponent was not possible with very large numbers. Finally, the output prediction is calculated. This will return a percentage for each classification with the closer the prediction is to 1 the more likely the network thinks the input falls under that category.

~~~ Python
def softmax(inputArray):
	#inputArray.astype(np.float64)
	inputArray -= np.max(inputArray)
	output = np.exp(inputArray) / np.sum(np.exp(inputArray))
	return output
~~~
