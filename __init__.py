from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators
import requests
import config
import os, codecs
import json

app = Flask(__name__)
app.secret_key = 'a_random_string_which_you_need_to_protect_your_custom_form_during_production'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test2.db'
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
	url = config.URL + '/auth.cgi?callback=http://788119bf.ngrok.io/callback&description=customforms'if config.LOGIN_METHOD else '/login'
	return render_template('index.html', url=url)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		r = requests.get(config.URL + '/rest/login?login=' + request.form['username'] + '&password=' + request.form['password'])
		if r.status_code == 200:
			print(r.json())
			# user = User(request.form['username'],r.json()[0],r.json()[1])
			session['token'] = r.json()[1]
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
		# content = request.get_json(force=True)
		# client_api_key = User.query.filter_by(rand_id=content['callback_result'], client_api_login=content['client_api_login']).first()
		# if(client_api_key):
		return 'Success'



@app.route('/form', methods=['GET', 'POST'])
def submit():
	form = CustomForm()
	if 'token' in session:
	    if request.method == 'POST':
	    	description = '\n>>Name' + '\n' + request.form['name'] + '\n>>Email' + '\n' + request.form['email'] + '\n>>I accept terms' + '\n' + request.form['terms'] 
	    	data = {
	    		'product' : 'IPC',
	    		'component' : 'Marketing',
	    		'version' : 'unspecified',
	    		'summary' : 'Custom Form Response',
	    		'description' : description
	    	}
	    	r = requests.post(config.URL + '/rest/bug?token=' + session['token'], data=data)
	    	return redirect('/')
	    return render_template('customform.html', form=form)
	else:
		return redirect('/')

#
#Main
#

if __name__ == '__main__':
	app.run()