from flask import Flask, render_template

app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config.prod.ProductionConfig')
@app.route('/')
def index():
    return 'Hello World'

@app.route('/hello')
def hello():
    return 'Hello W0rld'

@app.route('/sponsors')
def sponsors():
	# return 'hello sponsors'
	return render_template('sponsors.html')

@app.route('/register', method=['GET'])
def get_registration_page():
	#return registration page


@app.route('/accounts', method=['POST'])
def register_user():
	user_type = request['type']
	email_address  = request['email_address']
	hashed_password = request['password']
	## Rehash password
	## Check if user in DB -- return or update
	## Write to DB

if __name__ == '__main__':
    app.run(debug=True)





# class User(db.Model):
#     __tablename__ = 'hackers'
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(32), index = True)
#     password_hash = db.Column(db.String(128))
#     university = db.Column(db.String(32))



