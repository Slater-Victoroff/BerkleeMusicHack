import scipy.misc as sm
from scipy import ndimage as nd
import matplotlib as ml
import matplotlib.pyplot as plt

def image_difference(image1, image2, sigma=2, median=3):
	"""
	Outputs a numpy array that represents the elementwise difference between image1 and image2
	"""
	first = nd.gaussian_filter(sm.imread(image1, flatten=True), sigma=sigma)
	second = nd.gaussian_filter(sm.imread(image2, flatten=True), sigma=sigma)
	sizes = [min(pair) for pair in zip(first.shape, second.shape)]
	core_slices = tuple([slice(0,size) for size in sizes])
	difference = first[core_slices] - second[core_slices]
	return nd.median_filter(difference, median)

def display_array(array, output=None):
	"""
	Actively displays the given array as a colorplot
	"""
	plt.imshow(array)
	if output:
		sm.imsave(output, array)
	plt.show()

display_array(image_difference("globe1.png", "globe2.png"), "difference.png")
