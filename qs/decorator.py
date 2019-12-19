from flask import redirect, url_for, request, g

from datetime import datetime as dt

from urllib.parse import unquote
from collections import namedtuple

from . import fields



def set(defaults=None):

	QueryString = namedtuple('QueryString', ' '.join(defaults.keys()))

	def wrapper(func):

		def inner(*args, **kwargs):

			if defaults is None:
				return func(*args, **kwargs)
		
			fields_this_request = convert_qs_to_fields(request.args, defaults)

			if not all([i in fields_this_request for i in defaults]):

				response_fields = {k: fields_this_request.get(k, defaults.get(k))
								for k in defaults }
			else:
				response_fields = fields_this_request

			# Field dump is turned into a URL
			field_dump = {k: v.dump() for k,v in response_fields.items()}
			
			# g.qs retains Field objects for use in templates and app logic
			g.qs = QueryString(**response_fields)
			
			# If the format of request fields matches what we'd redirect to,
			# then don't redirect, just build the page
			if all([field_dump[k] == request.args.get(k)
					for k in field_dump.keys()]):

				return func(*args, **kwargs)

			# Otherwise, build a freshly formatted URL with all the default
			# vars and redirect to it.
			new_url = url_for(request.endpoint, **field_dump)
				
			# Unquote the URL in case special characters were %-ified
			unquoted = unquote(new_url)

			return redirect(unquoted)		

		return inner

	return wrapper


def convert_qs_to_fields(request_qs, default_fields):
	'''This method extracts values from Werkzeug's
	ImmutableDict of the query string variables.

	It tosses key-value-pairs not defined in default_fields.
	It converts the querystring strings into Field() objects.
	'''
	
	fields = {}

	for k in request_qs.keys():

		if k not in default_fields:
			continue

		try:

			if isinstance(default_fields[k], fields.ListField):
				fields[k] = type(default_fields[k])(request_qs.getlist(k))
			else:	
				valid_vars[k] = type(default_fields[k])(request_qs.get(k))
		except ValueError:
			pass

	return fields

