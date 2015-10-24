from __future__ import division

from page_classifier import imagetools

def all_attributes(image):
	"""Returns all decisive attributes of the image as a tuple. The attributes are the following, in order:
	- height of image
	- width of image
	- area of image
	- eccentricity of image (width / height)
	- ratio of black pixels to area
	- ratio of black pixels to area after applying RLSA
	- mean number of white-black transitions
	- count of black pixels
	- count of black pixels after applying RLSA
	- number of white-black transitions"""
	area = image.width * image.height
	black_pixels = count_black_pixels(image)
	transitions = count_transitions(image)
	rlsa = imagetools.rlsa_box(image, horizontal_threshold=80, vertical_threshold=80)
	black_pixels_rlsa = count_black_pixels(rlsa)
	return image.height, image.width, area, image.width / image.height, black_pixels / area, \
	       black_pixels_rlsa / area, black_pixels / (transitions + 1), black_pixels, black_pixels_rlsa, transitions

def count_black_pixels(image):
	n = 0
	for y in xrange(image.height):
		for x in xrange(image.width):
			if imagetools.is_pixel_black(image, x, y):
				n += 1
	return n
	
def count_transitions(image):
	n = 0
	for y in xrange(image.height):
		for x in xrange(image.width - 1):
			if not imagetools.is_pixel_black(image, x, y) and imagetools.is_pixel_black(image, x + 1, y):
				n += 1
	return n