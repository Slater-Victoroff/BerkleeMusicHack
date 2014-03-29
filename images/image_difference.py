import scipy.misc as sm
import matplotlib as ml
import matplotlib.pyplot as plt

def image_difference(image1, image2):
	"""
	Outputs a numpy array that represents the elementwise difference between image1 and image2
	"""
	first = sm.imread(image1)
	second = sm.imread(image2)
	sizes = [min(pair) for pair in zip(first.shape, second.shape)]
	core_slices = tuple([slice(0,size) for size in sizes])
	return first[core_slices] - second[core_slices]

def display_array(array, output=None):
	"""
	Actively displays the given array as a colorplot
	"""
	plt.imshow(array)
	if output:
		sm.imsave(output, array)
	plt.show()

display_array(image_difference("globe1.png", "globe2.png"), "difference.png")
