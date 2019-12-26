import pytest
from flask_querystring import fields as f


def test_inheritance():


	param = f.StringListField([])

	assert isinstance(param, f.ListField) and isinstance(param, f.Field)

def test_non_list_input_type():

	with pytest.raises(TypeError): 
		param = f.StringListField('')


def test_all_status_for_empty_list():

	param = f.StringListField([])

	assert param.blank

def test_empty_init():

	param = f.StringListField()

	assert param.blank


def test_empty_init_then_load():

	param1 = f.StringListField(['a', 'b', 'c'])
	
	param2 = f.StringListField()
	param2.load(['a', 'b', 'c'])

	assert param1 == param2


def test_dump():

	location = f.StringListField(['a', 'b', 'c'])

	assert location.dump() == 'a,b,c'


def test_dummy():

	param = f.StringListField()

	assert param.dummy == [str(int())]

