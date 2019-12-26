from .decorator import set as decorator_set
from .fields import *

from flask import current_app, _app_ctx_stack


class QueryStringValidator(object):

	def __init__(self, app=None):
		self.app = app
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		pass


	def teardown(self, exception):
		pass

	def set(self, *args, **kwargs):
		decorator_set(*args, **kwargs)

