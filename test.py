from __future__ import with_statement

from weka import classifiers
from weka.core.converters import ConverterUtils
from weka import core

def load_data(filename):
	conv = ConverterUtils.DataSource(filename)
	return conv.getDataSet(10)
	
def demo_tree(data, split_position=None):
	if split_position is None:
		split_position = data.numInstances() // 2
	c45 = classifiers.trees.J48()
	training_data = core.Instances(data, 0, split_position)
	test_data = core.Instances(data, split_position, data.numInstances() - split_position)
	for instance in test_data.enumerateInstances():
		if instance.classValue() == 0:
			instance.setClassMissing()
	test_data.deleteWithMissingClass()
	c45.buildClassifier(training_data)
	print(c45)
	ev = classifiers.Evaluation(training_data)
	ev.evaluateModel(c45, test_data)
	print ev.toSummaryString()
	
if __name__ == "__main__":
	import sys
	demo_tree(load_data(sys.argv[1]), None if len(sys.argv) < 3 else int(sys.argv[2]))