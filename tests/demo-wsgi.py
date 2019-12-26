from flask import Flask, render_template
from flask_querystring import QueryStringValidator
from flask_querystring.fields import DateField, IntegerListField, IntegerField
from flask_querystring.decorator import set as dec


app = Flask(__name__)

DEFAULTS = {
	'start': DateField('2019-10-01'),
	'end': DateField('2020-01-01'),
	'location': IntegerListField(),
	'customer': IntegerListField(),
	'supplier': IntegerListField(),
	'cutoff': IntegerField(7)
}

@dec(DEFAULTS)
def index():
	
	return render_template('index.html')



app.add_url_rule('/', 'home', index)
