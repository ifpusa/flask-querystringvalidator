from flask import Flask, render_template
import qs



app = Flask(__name__)


DEFAULTS = {
	'start': qs.fields.DateField('2019-10-01'),
	'end': qs.fields.DateField('2020-01-01'),
	'location': qs.fields.IntegerListField(),
	'customer': qs.fields.IntegerListField(),
	'supplier': qs.fields.IntegerListField(),
	'cutoff': qs.fields.IntegerField(7)
}



@qs.decorator.set(DEFAULTS)
def index():
	
	return render_template('index.html')



app.add_url_rule('/', 'home', index)
