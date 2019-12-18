from flask import redirect, url_for, request, g

from datetime import datetime as dt

from urllib.parse import unquote


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

				return redirect(
						unquote(
						url_for(request.endpoint, **formatted_vars)
						)
						)
			g.qs_vars = valid_vars
			
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

