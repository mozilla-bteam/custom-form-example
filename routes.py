from flask import Blueprint, session, render_template, request, redirect
from form.form_model import CustomForm
from models import User, db
import requests
import config
import os, codecs
import json

route = Blueprint('route', __name__)

@route.route('/')
def hello():
	url = config.URL + '/auth.cgi?callback=' + config.SITE_URL + '/callback&description=customforms'if config.LOGIN_METHOD else '/login'
	return render_template('index.html', url=url)

@route.route('/login', methods=['GET', 'POST'])
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

@route.route('/callback', methods=['GET', 'POST'])
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



@route.route('/form', methods=['GET', 'POST'])
def submit():
	if 'api_key' in session:
		form = CustomForm()
		if request.method == 'POST':
			description=''
			for label, value in form.data.items():
				description += '\n>>' + label + '\n' + str(value)
			data = {
			'product' : config.PRODUCT,
			'component' : config.COMPONENT,
			'version' : config.VERSION,
			'summary' : config.SUMMARY,
			'description' : description,
			'op_sys' : config.OS
			}
			print(description)
			r = requests.post(config.URL + '/rest/bug?api_key=' + session['api_key'], data=data)
			print(r.status_code)
			print(r.json())
			return redirect(config.URL + '/show_bug.cgi?id=' + str(r.json()['id']))
		return render_template('customform.html', form=form)
	else:
		return redirect('/')