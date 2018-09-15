from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_login import LoginManager

loginmanager=LoginManager()
loginmanager.session_protection='strong'
loginmanager.login_view='main.login'

app = Flask(__name__)
loginmanager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
#db.create_all()

class Blogpost(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	title = db.Column(db.String(50))
	subtitle = db.Column(db.String(50))
	author = db.Column(db.String(20))
	date_posted = db.Column(db.DateTime)
	content = db.Column(db.Text)

class User(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64))
	password=db.Column(db.String(28))

@loginmanager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/')
def index():
	posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
	return render_template('index.html',posts = posts)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
	post = Blogpost.query.filter_by(id=post_id).one()
	

	return render_template('post.html',post = post)

@app.route('/add')
def add():
	return render_template('add.html')

@app.route('/addpost',methods = ['POST'])
def addpost():
	title = request.form['title']
	subtitle = request.form['subtitle']
	author = request.form['author']
	content = request.form['content']

	post = Blogpost(title = title, subtitle = subtitle, author = author, content = content, date_posted = datetime.now())

	db.session.add(post)
	db.session.commit()

	return redirect(url_for('index'))

@app.route('/sign')
def sign():
	return render_template('sign.html')

@app.route('/signup',methods=['POST'])
def signup():
	username = request.form['username']
	password = request.form['password']

	user = User(username = username, password = password)

	db.session.add(user)
	db.session.commit()

	return redirect(url_for('index'))

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/log',methods=['GET','POST'])
def log():
	username = request.form['username']
	password = request.form['password']
	user = User.query.filter(User.username == username,
							 User.password == password).first()
	if user:
		return render_template('index.html')
	return render_template('login.html')

if __name__ == '__main__':
	app.run(debug = True)
