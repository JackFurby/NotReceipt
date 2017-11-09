For the CNN I used a guide which can be found here: http://cs231n.github.io/convolutional-networks/. This guide goes over how the CNN works and includes a small bit of numpy code. I won't go into as great detail as my main goal here is to document my code.

# Convolutional Layer

The convolutional layer has the input of an image, filter size, stride, padding, filter layers, filters and bias. The image will be a numpy array and in my case, will be 1 in depth for the first input as I am suing greyscale. My code does work for more layers however. The filter size just defines the width and height of the filter to be used. The stride is how many pixels will be convolving (slide) across the input image. 3 is the max that should be convolving with 1 being the minimum. padding is how many 0's will be added to each layer of the input image. Filter layers defines the depth of the output but will also state how many layers of filters will be used. The final 2 inputs are filters and bias which is where pre-defined filters and biases can be inputted. If these are left blank new filters and biases will be created.

~~~ Python
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
~~~

The first section of the convolution layer will check the inputs. If the width or height (W) minus the filter (F) width or height plus 2 times padding (P) all divided by the stride (S) plus 1 does not equals an int it will not be possible to complete this layer and the script will stop. If all is good however the output numpy array will be created with the values (W−F+2P)/S+1. The output will have a depth of filterLayers and contain values of type int. If any padding was specified it will also be added to the input image at this point.

~~~ Python
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
~~~

If filters and / or bias were blank the above code will create them. For the filters it will make some numpy arrays with the width and height of the input filter size with the depth of the input image depth. This will be repeated for the number of filter layers there are and each time the result will be added to the end of an array. The same is repeated for the bias but the numpy array is always 1x1x1.

~~~ Python
for i in range(outshape.shape[2]):  # number of filters
		filterArray = filters[i]
		for j in range(0, outshape.shape[1]):  # height of activation map
			for k in range(0, outshape.shape[0]):  # width of activation map
				outshape[k, j, i] = np.sum(image[k*stride:filterArray.shape[0] + k*stride, j*stride:filterArray.shape[1] + j*stride, :] * filterArray[:, :, :]) + bias[i]
		return outshape, filters, bias # retult, filiters and bias returned
~~~

Finally, we get onto the convolve section. Here the image is convolved with each time the section of the image being looked at Element-wise multiplication will be applied to the filter with the bias being added on at the end. The result will be summed up and added to the output matrix. Once complete the output, filters and bias will be returned.
