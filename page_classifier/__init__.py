import optparse
import os
import mimetypes
from page_classifier import dataset, imagetools, ui

def classify(dataset_fname, image_fname):
	c = dataset.Classifier(dataset_fname)
	c.build()
	print c.classify_one(imagetools.load(image_fname))
	
def generate(dataset_fname, image_dir):
	data = dataset.Classifier("page-blocks.data", blank=True)
	for image_file in os.listdir(image_dir):
		if os.path.isdir(image_file):
			continue
		file_type = mimetypes.guess_type(image_file)[0]
		if file_type is not None and file_type.startswith("image/"):
			image = imagetools.load(os.path.join(image_dir, image_file))
			chosen_class_name = ui.classify_image(image)
			data.add(image, dataset.CLASS_NAMES.index(chosen_class_name))
	data.write_to(dataset_fname)

def evaluate(training_dataset_fname, testing_dataset_fname):
	train = dataset.Classifier(training_dataset_fname)
	test = dataset.Classifier(testing_dataset_fname)
	train.build()
	train.test_against(test)

def evaluate_self(dataset_fname, training_fraction="0.5"):
	c = dataset.Classifier(dataset_fname)
	c.test_against_self(training_fraction=float(training_fraction))

if __name__ == "__main__":
	parser = optparse.OptionParser()
	options, args = parser.parse_args()
	globals()[args[0].replace("-", "_")](*args[1:])
	if len(args) < 3:
		print "positional arguments: {classify | generate | evaluate} dataset-file <image, dir of images, or dataset-file>"
	else:
		pass