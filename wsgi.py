from flask import Flask, render_template
import qs



app = Flask(__name__)


DEFAULTS = {
	'start': qs.fields.Date('2019-10-01'),
	'end': qs.fields.Date('2020-01-01'),
	'location': qs.fields.List('all'),
	'customer': qs.fields.String('all'),
	'supplier': qs.fields.String('all'),
	'cutoff': qs.fields.Integer(7)
}



@qs.decorator.set(DEFAULTS)
def index():

	breakpoint()
	
	return render_template('index.html')



app.add_url_rule('/', 'home', index)


