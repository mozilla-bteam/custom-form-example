from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

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