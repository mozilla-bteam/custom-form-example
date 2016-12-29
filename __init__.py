from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, RadioField, TextAreaField, SelectField, SelectMultipleField
from wtforms import validators
import requests
import config
import os, codecs
import json

app = Flask(__name__)
app.secret_key = 'a_random_string_which_you_need_to_protect_your_custom_form_during_production'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.dirname(os.path.abspath(__file__)) +'/sqlite3.db'
print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)

#
#Form Models
#

class LoginForm(FlaskForm):
	username = StringField('Username', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])

class CustomForm(FlaskForm):
	name = StringField('Name', [validators.DataRequired(), validators.Length(min=4, max=25)])
	email = StringField('Email Address', [validators.Length(min=6, max=35)])
	dob = DateField('Date of Birth', format='%m/%d/%Y')
	lang = RadioField('Your Primary Language', choices=[('english','English'),('french','French'),('spanish','Spanish'),('portugese','Portugese'),('hindi','Hindi')])
	tier = SelectField('Your Tier?', choices=[(1, "One"), (2, "Two"), (2, "Three")], default=1)
	gears = SelectMultipleField('Gears you want?', choices=[('shirt', "Firefox Shirt"), ('cap', "Firefox Cap"), ('hoodie', "Mozilla Hoodie")],)
	comments = TextAreaField('Any Comments?', [validators.DataRequired()])
	terms = BooleanField('I accept terms', [validators.DataRequired()])

#
#Database Models
#

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rand_id = db.Column(db.String(80))
	client_api_login = db.Column(db.String(120))
	client_api_key = db.Column(db.String(120))

	def __init__(self, rand_id, client_api_login, client_api_key):
		self.rand_id = rand_id
		self.client_api_login = client_api_login
		self.client_api_key = client_api_key

	def __repr__(self):
		return '<User %r>' % self.rand_id

#
#Routes
#

@app.route('/')
def hello():
	url = config.URL + '/auth.cgi?callback=' + config.SITE_URL + '/callback&description=customforms'if config.LOGIN_METHOD else '/login'
	return render_template('index.html', url=url)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		r = requests.get(config.URL + '/rest/login?login=' + request.form['username'] + '&password=' + request.form['password'])
		if r.status_code == 200:
			print(r.json())
			# user = User(request.form['username'],r.json()[0],r.json()[1])
			session['api_key'] = r.json()[1]
			redirect('/form')
		print(r.status_code)
	return render_template('loginform.html', form=form, url=config.URL)

@app.route('/callback', methods=['GET', 'POST'])
def callback():
	if request.method == 'POST':
		content = request.get_json(force=True)
		if (content):
			client_api_login = content['client_api_login']
			client_api_key = content['client_api_key']

		if (client_api_key and client_api_login):
			rand_id = codecs.encode(os.urandom(16),'hex').decode()
			user = User(rand_id, client_api_login, client_api_key)
			db.session.add(user)
			db.session.commit()
			return json.dumps({'result' : rand_id})

	elif request.method == 'GET':
		client_api_key = User.query.filter_by(rand_id=request.args.get('callback_result'), client_api_login=request.args.get('client_api_login')).first().client_api_key
		if(client_api_key):
			session['api_key'] = client_api_key
			return redirect('/form')



@app.route('/form', methods=['GET', 'POST'])
def submit():
	if 'api_key' in session:
		form = CustomForm()
		if request.method == 'POST':
			description=''
			for label, value in form.data.items():
				description += '\n>>' + label + '\n' + str(value)
			data = {
			'product' : 'Firefox',
			'component' : 'General',
			'version' : 'unspecified',
			'summary' : 'Custom Form Response',
			'description' : description,
			'op_sys' : 'Mac OS X'
			}
			print(description)
			r = requests.post(config.URL + '/rest/bug?api_key=' + session['api_key'], data=data)
			print(r.status_code)
			print(r.json())
			return redirect(config.URL + '/show_bug.cgi?id=' + str(r.json()['id']))
		return render_template('customform.html', form=form)
	else:
		return redirect('/')

#
#Main
#

if __name__ == '__main__':
	app.run()