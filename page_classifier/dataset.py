"""This module contains functions that allow the creation, loading and storage of data sets."""

from weka.classifiers import trees
from weka import core, classifiers
from weka.core.converters import ConverterUtils
from page_classifier import attributes

CLASS_NAMES = ["text", "horizontal line", "picture", "vertical line", "graphic"]

class Classifier(object):
	"""This class represents an image classifier which can be seeded from an existing dataset or built at runtime."""
	
	def __init__(self, filename, blank=False):
		"""Creates a new classifier based on the data from the specified file. If blank is true, only the
		headers of the data are used, and the dataset is left empty; otherwise, all of the data in the file are
		loaded."""
		self.c45 = trees.J48()
		source = ConverterUtils.DataSource(filename)
		if blank:
			self.dataset = source.structure
		else:
			self.dataset = source.dataSet
		self.dataset.setClassIndex(self.dataset.numAttributes() - 1)
	
	def add(self, image, class_):
		"""Adds a new pre-classified image to this classifier's dataset."""
		self.dataset.add(self.instance_for(image, class_))
	
	def instance_for(self, image, class_=None):
		"""Generates an instance corresponding to the given image. The instance does not initially have a class value,
		unless the class_ argument is passed to specify one."""
		instance = core.Instance(self.dataset.numAttributes())
		instance.setDataset(self.dataset)
		attrset = attributes.all_attributes(image)
		for i, attr in enumerate(attrset):
			instance.setValue(i, attr)
		if class_ is not None:
			instance.setClassValue(class_)
		return instance
	
	def build(self):
		"""Builds the decision tree for this classifier."""
		self.c45.buildClassifier(self.dataset)
	
	def classify_one(self, image):
		"""Classifies the given image according to this classifier's decision tree and returns a string
		describing the computed type of the image."""
		return CLASS_NAMES[int(self.c45.classifyInstance(self.instance_for(image)))]
	
	def test_against(self, test):
		"""Tests this classifier using another Classifier's dataset as test data. Prints the results of the
		test on the console."""
		evaluator = classifiers.Evaluation(self.dataset)
		evaluator.evaluateModel(self.c45, test.dataset)
		print evaluator.toSummaryString()
		
	def test_against_self(self, training_fraction=0.5):
		"""Tests this classifier using part of its own dataset as test data. Otherwise behaves as test_against.
		The portion of the dataset to be used as training data may be given by the training_fraction parameter;
		if not, it is 0.5 by default."""
		training_size = int(self.dataset.numInstances() * training_fraction)
		training_data = core.Instances(self.dataset, 0, training_size)
		test_data = core.Instances(self.dataset, training_size, self.dataset.numInstances() - training_size)
		evaluator = classifiers.Evaluation(training_data)
		c45 = trees.J48()
		c45.buildClassifier(training_data)
		evaluator.evaluateModel(c45, test_data)
		print evaluator.toSummaryString()
		
	def write_to(self, fname):
		"""Writes this classifier's dataset to the given file."""
		ConverterUtils.DataSink(fname).write(self.dataset)