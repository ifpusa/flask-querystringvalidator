from flask import redirect, url_for, request

from datetime import datetime as dt

def mandatory_params(defaults=None):

	def wrapper(func):

		def inner(*args, **kwargs):

			if defaults is None:
				return func(*args, **kwargs)

			valid_vars = validate_vars(request.args, defaults)

			if not all([i in valid_vars for i in defaults]):

				request_p = {k: valid_vars.get(k, defaults.get(k))
								for k in defaults }

				formatted_vars = {k: str(v) for k,v in request_p.items()}
				return redirect(url_for(request.endpoint, **formatted_vars))
				
			return func(*args, **kwargs)


		return inner

	return wrapper


def validate_vars(vars, defaults):
	
	valid_vars = {}

	for k in vars:

		try:
			valid_vars[k] = type(defaults[k])(vars.get(k))
		except ValueError:
			pass

	return valid_vars

class QsParam(object):

	def __init__(self, value):

		self.value = value

	def __str__(self):

		return str(self.value)


class URLDate(QsParam):

	ALLOWED_FORMATS = ['%Y%m%d', '%Y-%m-%d']

	def __init__(self, value):

		self.value = None

		for fmt in URLDate.ALLOWED_FORMATS:

			try:
				self.value = dt.strptime(value, fmt)
			except ValueError:
				pass

		if self.value is None:
			raise ValueError('Not a valid date format!')


	def __str__(self):

		return dt.strftime(self.value, URLDate.ALLOWED_FORMATS[0])


class URLString(QsParam):

	def __init__(self, *args, **kwargs):
		QsParam.__init__(self, *args, **kwargs)


class URLInteger(QsParam):

	def __init__(self, value):
		self.value = int(value)

class URLList(QsParam):

	def __init__(self, *args, **kwargs):

		QsParam.__init__(self, *args, **kwargs)

	def __str__(self):

		return '[' + ','.join([str(i) for i in self.value]) + ']'
