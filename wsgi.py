from flask import Flask, request, url_for, redirect
from datetime import datetime, timedelta

import validators
from page_params import mandatory_params, URLDate, URLString, URLInteger, URLList


app = Flask(__name__)


DEFAULTS = {
	'start': URLDate('2019-10-01'),
	'end': URLDate('2020-01-01'),
	'location': URLString('all'),
	'customer': URLString('all'),
	'supplier': URLString('all'),
	'cutoff': URLInteger(7),
	'col': URLList([i for i in range(10)])
}
	





@mandatory_params(DEFAULTS)
def index():

	return 'hello world!'



app.add_url_rule('/', 'home', index)


