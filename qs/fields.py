from datetime import datetime


class Field(object):

	def __init__(self, t):

		self.t = t
		self.value = None


	def ok_type(self, input):
		'''Compares the input arg against the declared type of this field.
		'''

		return isinstance(input, self.t)

	def dump(self):

		if self.value is None:
			return ''

		return self.format(self.value)

	def format(self, x):
		'''This method can be overridden by subclasses'''

		raise NotImplementedError("Format functions must be written by subclasses.")

	@property
	def blank(self):
		return self.value is None

	@property
	def dummy(self):
		'''This is built for tie-in's with SQLAlchemy expanding bindparams.
		The DBAPI expects an input list of strongly typed values.

		Returns a list of length 1 with a single raw value.
		'''

		return self.t()

	def __eq__(self, other):

		return self.value == other.value
	

class IntegerField(Field):

	def __init__(self, value=None):
		Field.__init__(self, t=int)

		if value is None:
			return

		self.load(value)


	def load(self, val):

		# If the passed in value is of the correct type
		# Save it and return
		if self.ok_type(val):
			self.value = val
			return

		if val is '':
			return

		# Otherwise we try to coerce it
		try:
			self.value = self.t(val)
		except ValueError:
			raise TypeError(f"Value must be of type string or {self.t}.")
		else:
			return

	def format(self, val):

		return str(val)


class DateField(Field):

	ALLOWED_FORMATS = ['%Y%m%d', '%Y-%m-%d']

	def __init__(self, value=None):
		Field.__init__(self, t=datetime)

		if value is None:
			return

		self.load(value)


	def load(self, val):

		# If the passed in value is of the correct type
		# Save it and return
		if self.ok_type(val):
			self.value = val
			return

		# If it's not the correct type, the only other option is string.
		if not isinstance(val, str):
			raise TypeError("Value must be of type string.")

		# Otherwise we try to coerce it
		for fmt in DateField.ALLOWED_FORMATS:
			try:
				self.value = datetime.strptime(val, fmt)
			except ValueError:
				continue

		if self.value is None:
			raise TypeError(f"Value must be a valid ISO8601 date string or {self.t}.")

	def format(self, x):
		'''This method can be overridden by subclasses'''

		return self.value.strftime(DateField.ALLOWED_FORMATS[0])

	@property
	def dummy(self):
		return datetime(year=1900, month=1, day=1)


class ListField(Field):

	def __init__(self, t, value):
		'''
		t: a type object like str, list, dict, or tuple
		'''

		Field.__init__(self, t=t)


		if value is None or value == []:
			return

		self.load(value)

		

	def load(self, this_input):

		if not isinstance(this_input, list):
			raise TypeError("ListField Fields only accept arguments of type list()")

		if all([self.ok_type(i) for i in this_input]):
			self.value = [i for i in this_input]
			return

		filtered_list = [i for i in filter(lambda x: x != '', this_input)]

		try:
			self.value = [self.t(i) for i in filtered_list]
		except ValueError: # I'm not entirely sure how to test this assertion
			raise TypeError(f"This list field accepts strings or {self.t}.")
		else:
			return


	def dump(self, sort_values=True):

		# TODO: Make it possible to set the "blank" value for a ListField
		if self.value is None:
			return ''

		fmt_values = [self.format(i) for i in self.value]

		if sort_values:
			return ','.join(sorted(fmt_values))
		else:
			return ','.join(fmt_values)

	def format(self, val):

		return str(val)

	@property
	def dummy(self):
		'''This is built for tie-in's with SQLAlchemy expanding bindparams.
		The DBAPI expects an input list of strongly typed values.

		Returns a list of length 1 with a single raw value.
		'''

		return [self.t()]


	def __eq__(self, other):

		if not hasattr(other, 'value'):
			return False

		return list(sorted(self.value)) == list(sorted(other.value))


class IntegerListField(ListField):

	def __init__(self, value=None):
		ListField.__init__(self, t=int, value=value)

	@property
	def dummy(self):
		return [int()]
	


class StringListField(ListField):

	def __init__(self, value=None):
		ListField.__init__(self, t=str, value=value)

	@property
	def dummy(self):
		return [str(int())]
