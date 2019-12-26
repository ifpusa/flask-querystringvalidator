import pytest
from datetime import datetime
from flask_querystring import fields as f


def test_inheritance():

	param = f.DateField()

	assert isinstance(param, f.Field)

def test_non_int_input():

	with pytest.raises(TypeError):
		param = f.DateField(1)

def test_empty_init():

	param = f.DateField()

	assert param.blank


def test_empty_init_then_load():

	param1 = f.DateField('1900-01-01')
	
	param2 = f.DateField()
	param2.load('1900-01-01')

	assert param1 == param2


def test_dump():

	param = f.DateField('1900-01-01')

	assert param.dump() == '19000101'


def test_dummy():

	param = f.DateField()

	assert param.dummy == datetime(year=1900, month=1, day=1)

