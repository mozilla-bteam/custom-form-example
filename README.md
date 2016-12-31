#Custom Form Example
This application is made using Flask. Visit [https://bugzilla-mozilla.herokuapp.com](https://bugzilla-mozilla.herokuapp.com).

## Form Customization
To customize the form, two files need to be changed - `config.py` and `form/form_model.py`


* `form/form_model.py` - Contains the structure of the form. Types of fields are mentioned [here](https://www.tutorialspoint.com/flask/flask_wtf.htm), though almost all have been covered in this example form.


* `config.py` - All the variables required to deploy the app

##Installation

###Running Locally
```shell

#Clone the repository
$ git clone https://github.com/mozilla-bteam/custom-form-example customforms
$ cd customforms

#Install dependencies and start the app
$ pip3 install -r requirements.txt
$ gunicorn __init__:app

```

###Deployment Instruction
This app is configured to be easily deployable on heroku.

Setup the heroku app (after installing Heroku Toolbelt). [This might help](https://coderwall.com/p/pstm1w/deploying-a-flask-app-at-heroku)

```
$ heroku create <app name>
$ git push heroku master
```


##UI
![Form Style](https://cloud.githubusercontent.com/assets/13795788/21542123/a1ace0c0-cde1-11e6-98b1-01efacd4922f.png)
