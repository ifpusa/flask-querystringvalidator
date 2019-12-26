import pytest
from flask_querystring import fields as f


def test_inheritance():

	param = f.IntegerListField([])

	assert isinstance(param, f.ListField) and isinstance(param, f.Field)

def test_non_list_input_type():

	with pytest.raises(TypeError): 
		param = f.IntegerListField('')

def test_non_homogenous_list():

	with pytest.raises(TypeError):
		param = f.IntegerListField([1, 'a'])

def test_all_status_for_empty_list():

	param = f.IntegerListField([])

	assert param.blank

def test_empty_init():

	param = f.IntegerListField()

	assert param.blank


def test_empty_init_then_load():

	param1 = f.IntegerListField([1,2,3])
	
	param2 = f.IntegerListField()
	param2.load([1,2,3])

	assert param1 == param2


def test_dump():

	location = f.IntegerListField([10,20,30,40,50])

	assert location.dump() == '10,20,30,40,50'


def test_dummy():

	param = f.IntegerListField()

	assert param.dummy == [int()]

def test_dump_empty_list():

	param = f.IntegerListField()

	assert param.dump() == ''

def test_filter_empty_string_list_contents():

	param = f.IntegerListField(['','','',1])

	assert param.dump() == '1'

