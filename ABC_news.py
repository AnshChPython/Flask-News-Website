from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json

with open('config.json', 'r') as c:
    param = json.load(c)['params']

local_host = param['local_server']

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_POST='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=param['gmail-id'],
    MAIL_PASSWORD=param['gmail-password']
)
mail = Mail(app)
if local_host:
    app.config['SQLALCHEMY_DATABASE_URI'] = param['local_uri']
elif not local_host:
    app.config['SQLALCHEMY_DATABASE_URI'] = param['prod_uri']
else:
    raise 'can not find uri'
db = SQLAlchemy(app)


class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    user_password = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    user_phone_number = db.Column(db.String(13), nullable=False)
    date = db.Column(db.String(6), nullable=False)


class Post(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(6), nullable=False)
    posted_by = db.Column(db.String(20), nullable=False)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    query = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(6), nullable=False)


@app.route('/')
def home():
    temp = Post.query.filter_by().all()
    return render_template('HomePage.html', template=temp)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['POST','GET'])
def contacts():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        query = request.form.get('query')

        entry = Contacts(name=name, email=email, query=query, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')

# @app.route('/post/<string:p>')
# def post(post-slug):
# ret
# # @app.route('/add', methods=['GET', 'POST'])
# def add():
#     if request.method == 'POST':
#         title = request.form.get('title')
#         subtitle = request.form.get('subtitle')
#         content = request.form.get('content')
#         category = request.form.get('category')
#         by = request.form.get('posted_by')
#         entry = Post(title=title, subtitle=subtitle, content=content, category=category, date=datetime.now(), posted_by=by)
#         db.session.add(entry)
#         db.session.commit()
#     return render_template('add.html')


@app.route('/post/<string:post_slug>')
def post(post_slug):
    news_post = Post.query.filter_by(slug=post_slug).first()
    return render_template('post.html', post=news_post)


app.run(host='0.0.0.0', port=500, debug=True)
