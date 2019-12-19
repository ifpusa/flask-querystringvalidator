from flask import redirect, url_for, request, g

from datetime import datetime as dt

from urllib.parse import unquote
from collections import namedtuple

from . import fields

def first(iterable):

	return next(iter(iterable))


def set(defaults=None, mod=None):

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
			
			# TODO: Write a test that checks what happens when params are URL encoded
			# 		I'd like to remove URL encoded values to make the URL more readable
			#		but the urldecode functions in Werkzeug make that near impossible
			#		Might want to see if I can write my own but borrow some of the test
			#		definitions form the Werkzeug codebase.
					
			# If the format of request fields matches what we'd redirect to,
			# then don't redirect, just build the page
			if all([field_dump[k] == request.args.get(k)
					for k in field_dump.keys()]):

				return func(*args, **kwargs)

			# Otherwise, build a freshly formatted URL with all the default
			# vars and redirect to it.
			new_url = url_for(request.endpoint, mod=mod, **field_dump)

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

	parsed_fields = {}

	for k in request_qs.keys():

		if k not in default_fields:
			continue

		try:

			# ftype == field type (such as Integer, String, Date etc.)
			ftype = type(default_fields[k])
			_get_val = request_qs.get(k)

			# Non ListField types are easy because the whole querystring
			# value is passed to the Field constructor
			if not isinstance(ftype(), fields.ListField):
				parsed_fields[k] = ftype(_get_val)
				continue

			# At this point we know that the querystring schema expects
			# a list will be passed to the constructor.

			# This logic handles if a form was used to pass
			# a multiselect. In which case the query string will
			# have multiple key-value-pairs for each selected field
			# value: ?field=value1&field=value2&field=value3

			# It also handles requests with a hand-formed query string
			# like this: ?value1,value2,value3

			# ImmutableDict.getlist() returns a list even if a single value
			# was present. This logic confirms that a form was used
			# to prepare the querystring.

			_getlist_val = request_qs.getlist(k)

			_sent_by_hand = len(_getlist_val) == 1 and first(_getlist_val) == _get_val
			_sent_by_form = not _sent_by_hand

			if _sent_by_hand:
				field_constructor_list = _get_val.split(',')
			if _sent_by_form:
				field_constructor_list = _getlist_val

			if field_constructor_list == ['']:
				parsed_fields[k] = ftype()
			else:
				parsed_fields[k] = ftype(field_constructor_list)

		except ValueError:
			pass

	return parsed_fields
