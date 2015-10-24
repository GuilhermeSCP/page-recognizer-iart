"""This module provides an implementation of the RLSA (Run-Length Smoothing Algorithm)
for images that support the Java BufferedImage interface. The RLSA draws black pixels between any two black pixels
that are horizontally or vertically separated by no more than a certain threshold (which may be passed to the
RLSA functions)"""

from javax import swing, imageio
from java import io

def _signedvalue(x):
	if x & 0x80000000:
		return int(x - 0x100000000)
	return int(x)

BLACK = _signedvalue(0xFF000000)
WHITE = _signedvalue(0xFFFFFFFF)

__all__ = ["rlsa_horizontal", "rlsa_vertical", "rlsa_box", "pixel_and", "copy", "is_pixel_black", "display"]

def load(name):
	"""Returns a BufferedImage object with the contents of the image at the file with the given name."""
	return imageio.ImageIO.read(io.File(name))

def rlsa_horizontal(image, threshold=10):
	"""Applies the RLSA to image in the horizontal direction only and returns the result as a new image."""
	return _rlsa(image, iterpos=_iterpos_horizontal, reorder=lambda x, y: (x, y), threshold=threshold)

def rlsa_vertical(image, threshold=20):
	"""Applies the RLSA to image in the vertical direction only and returns the result as a new image."""
	return _rlsa(image, iterpos=_iterpos_vertical, reorder=lambda x, y: (y, x), threshold=threshold)

def rlsa_box(image, horizontal_threshold=10, vertical_threshold=20):
	"""Applies the RLSA to image in both directions, ANDs the results with pixel_and, then smooths again
	horizontally."""
	return rlsa_horizontal(pixel_and(rlsa_horizontal(image, horizontal_threshold), rlsa_vertical(image, vertical_threshold)),
						   horizontal_threshold)

def pixel_and(image1, image2):
	"""Returns an image which is the pixel-wise AND of image1 and image2: each pixel of the result is black
	if both corresponding pixels in image1 and image2 are black."""
	if image1.width != image2.width or image1.height != image2.height or image1.type != image2.type:
		raise TypeError("image sizes or types do not match")
	result = type(image1)(image1.width, image1.height, image1.type)
	for y in xrange(image1.height):
		for x in xrange(image1.width):
			if is_pixel_black(image1, x, y) and is_pixel_black(image2, x, y):
				value = BLACK
			else:
				value = WHITE
			result.setRGB(x, y, value)
	return result

def _iterpos_horizontal(image):
	for y in xrange(image.height):
		for x in xrange(image.width):
			yield x, y

def _iterpos_vertical(image):
	for x in xrange(image.width):
		for y in xrange(image.height):
			yield y, x

def _rlsa(image, iterpos, reorder, threshold=8):
	"""Applies the RLSA to image, iterating through pixels in the order specified by iterpos, which
	returns an iterator whose values are (i, j) tuples, where i is the index within the current line
	and j is the line index. reorder should be either the identity function or a function that returns its
	two arguments in reverse order.
	Returns a copy of the image with the RLSA applied."""
	new_image = copy(image)
	for i, j in iterpos(image):
		if i == 0:
			i_of_last_black = None
		if is_pixel_black(image, *reorder(i, j)):
			# Merge nearby black pixels
			if i_of_last_black is not None and i - i_of_last_black <= threshold:
				for k in xrange(i_of_last_black + 1, i):
					x, y = reorder(k, j)
					new_image.setRGB(x, y, BLACK)
			i_of_last_black = i
	return new_image

def copy(image):
	"""Returns a copy of the given image."""
	return type(image)(image.colorModel, image.copyData(None), image.alphaPremultiplied, None)

def is_pixel_black(image, x, y):
	return is_color_black(decompose_color(image.getRGB(x, y)))

def decompose_color(color):
	"""Decomposes the given color, which should be a 32-bit integer of the form ABGR, from most to least
	significant byte, into a tuple of (R, G, B) components, which will be ints in the range 0-255."""
	return color & 0xFF, (color & 0xFF00) >> 8, (color & 0xFF0000) >> 16

def is_color_black(color):
	"""Returns True if the given color (as a (R, G, B) tuple, where R, G and B are ints in the range 0-255)
	is to be considered black for the purposes of the RLSA. This is done by calculating the color's average
	brightness."""
	r, g, b = color
	return (r + g + b) / 3.0 < 128

def display(image, title=""):
	"""Opens a window displaying the given image (which may be an Image object or the file name of an image).
	Closing the window will not terminate the program."""
	window = swing.JFrame(title)
	window.defaultCloseOperation = swing.JFrame.DISPOSE_ON_CLOSE
	window.add(swing.JLabel(swing.ImageIcon(image)))
	window.pack()
	window.visible = True 
