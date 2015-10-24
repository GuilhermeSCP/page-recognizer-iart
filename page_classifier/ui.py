from __future__ import with_statement

"""This module implements the user interface for manually classifying images."""

import threading
from javax import swing

CLASS_NAMES = ["text", "horizontal line", "picture", "vertical line", "graphic"]

def classify_image(image):
	"""Displays a window that allows the user to view and classify an image."""
	frame = swing.JFrame()
	frame.defaultCloseOperation = swing.JFrame.DO_NOTHING_ON_CLOSE
	frame.add(swing.JLabel(swing.ImageIcon(image)))
	frame.add(swing.JLabel("Enter one of " + ", ".join(CLASS_NAMES)))
	frame.layout = swing.BoxLayout(frame.contentPane, swing.BoxLayout.Y_AXIS)
	class_field = swing.JTextField()
	classify_button = swing.JButton("Classify")
	condition = threading.Condition()
	def listener(_event):
		if class_field.text in CLASS_NAMES:
			with condition:
				condition.notifyAll()
		else:
			swing.JOptionPane.showMessageDialog(frame, "Image type is not one of the recognized types", "Input error",
											    swing.JOptionPane.ERROR_MESSAGE)
	class_field.addActionListener(listener)
	classify_button.addActionListener(listener)
	frame.add(class_field)
	frame.add(classify_button)
	frame.pack()
	frame.visible = True
	with condition:
		condition.wait()
	frame.dispose()
	return class_field.text