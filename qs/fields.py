from datetime import datetime as dt

'''

QsTypes are objects of defined type. They know three things:

1. What type of data they can hold
2. A value that has been provided
3. How to serialize that value to a URL query string parameter

Arguments to any subclass of QsType are always strings. Because they are usually populated from the URL bar.

Usage: 

1. Create a dictionary of default values for parameters
2. The keys will be string parameter names. The values will be subclasses of QsType


'''

import re


class QsType(object):

	def __init__(self, value):

		self.value = value

	def __str__(self):

		return str(self.value)

	def __repr__(self):
		return '<QsType Object: Value = ' + str(self.value) + '>'


class Date(QsType):

	ALLOWED_FORMATS = ['%Y%m%d', '%Y-%m-%d']

	def __init__(self, value):

		self.value = None

		for fmt in Date.ALLOWED_FORMATS:

			try:
				self.value = dt.strptime(value, fmt)
			except ValueError:
				pass

		if self.value is None:
			raise ValueError('Not a valid date format!')


	def __str__(self):

		return dt.strftime(self.value, Date.ALLOWED_FORMATS[0])


class String(QsType):

	def __init__(self, *args, **kwargs):
		QsType.__init__(self, *args, **kwargs)


class Integer(QsType):

	def __init__(self, value):
		self.value = int(value)


class List(QsType):

	def __init__(self, value):

		pattern = re.compile(r'[\[\] ]')
		splitable = re.sub(pattern, '', value)

		self.value = splitable.split(',')


	def __str__(self):

		if len(self.value) == 1:
			return f'[{self.value[0]}]'
		if len(self.value) == 0:
			return f'[]'
		if len(self.value) > 1:
			return f"[{','.join(self.value)}]"
