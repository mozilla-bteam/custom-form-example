from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, RadioField, TextAreaField, SelectField, SelectMultipleField
from wtforms import validators

CustomForm = type('CustomForm', (FlaskForm,) ,{
		'name': StringField('Name', [validators.DataRequired(), validators.Length(min=4, max=25)]),
		'email': StringField('Email Address', [validators.Length(min=6, max=35)]),
		'dob': DateField('Date of Birth', format='%m/%d/%Y'),
		'lang': RadioField('Your Primary Language', choices=[('english','English'),('french','French'),('spanish','Spanish'),('portugese','Portugese'),('hindi','Hindi')]),
		'tier': SelectField('Your Tier?', choices=[(1, "One"), (2, "Two"), (2, "Three")], default=1),
		'gears': SelectMultipleField('Gears you want?', choices=[('shirt', "Firefox Shirt"), ('cap', "Firefox Cap"), ('hoodie', "Mozilla Hoodie")],),
		'comments': TextAreaField('Any Comments?', [validators.DataRequired()]),
		'terms': BooleanField('I accept terms', [validators.DataRequired()])
	})