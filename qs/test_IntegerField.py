import pytest
import fields as f


def test_inheritance():

	param = f.IntegerField()

	assert isinstance(param, f.Field)

def test_non_int_input():

	with pytest.raises(TypeError): 
		param = f.IntegerField('a')

def test_empty_init():

	param = f.IntegerField()

	assert param.blank


def test_empty_init_then_load():

	param1 = f.IntegerField(1)
	
	param2 = f.IntegerField()
	param2.load(1)

	assert param1 == param2


def test_dump():

	location = f.IntegerField(1)

	assert location.dump() == '1'


def test_dummy():

	param = f.IntegerField()

	assert param.dummy == int()

