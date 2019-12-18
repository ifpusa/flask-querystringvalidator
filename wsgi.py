from flask import Flask, request, url_for, redirect,g
from datetime import datetime, timedelta

import validators
from page_params import mandatory_params

import qs_types


app = Flask(__name__)


DEFAULTS = {
	'start': qs_types.Date('2019-10-01'),
	'end': qs_types.Date('2020-01-01'),
	'location': qs_types.String('all'),
	'customer': qs_types.String('all'),
	'supplier': qs_types.String('all'),
	'cutoff': qs_types.Integer(7),
	'col': qs_types.List([i for i in range(10)])
}



@mandatory_params(DEFAULTS)
def index():


	return str(g.qs_vars)



app.add_url_rule('/', 'home', index)


