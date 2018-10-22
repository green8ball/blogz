from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import re
import hashlib

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, title, body, owner_id):
        self.title = title
        self.body = body
        self.owner_id = owner_id

    def __repr__(self):
        return '<Blog %r>' % self.title

@app.route('/blog/newpost', methods=['GET', 'POST'])
def newpost():
    title_error = "Title cannot be blank"
    body_error = "Body cannot be blank"
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title != "" and body != "":
            db.session.add(Blog(title, body, User.query.filter_by(username=session['username']).first().id))
            db.session.commit()
            return redirect("/blog?id=" + str(len(Blog.query.all())))
        else:
            return render_template('newpost.html',title=title, body=body, title_error="" if title != "" else title_error, body_error="" if body !="" else body_error)
    if request.method == 'GET':
        return render_template('newpost.html')

@app.before_request('login')
def require_login():


@app.route("/signup", methods=['POST','GET'])
def create_user():

    error_field_blank = "Error: Field blank"
    error_password_mismatch = "Error: Password Mismatch"
    error_password_invalid = "Error: Password Invalid"
    error_username_invalid = "Error: Invalid Username"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:

            is_username_valid = re.match("^([a-zA-Z0-9@*#]{3,20})$", username)
            is_password_valid = re.match("^([a-zA-Z0-9@*#]{3,20})$", password)
            
            if is_username_valid == None or username == "" or is_password_valid == None or password != verify or password == "":
                return render_template("signup.html",username = username, username_error = error_field_blank if username == "" else error_username_invalid if is_username_valid == None else "" , 
                                        password = "", password_error = error_field_blank if password == "" else error_password_mismatch if password != verify else error_password_invalid if is_password_valid == None else "",
                                        verify = "", verify_error = error_field_blank if verify == "" else error_password_mismatch if password != verify else error_password_invalid if is_password_valid == None else "")
            else:
                db.session.add(User(username, pw_encrypt(password)))
                db.session.commit()
                session['username'] = username
                return redirect('/blog/newpost')
        else:
            return render_template("signup.html",username = username, username_error="Username already exists!")
    else:
        return render_template("signup.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and pw_valid(password, user.password):
            session['username'] = username
            return redirect('/blog/newpost')
    if request.method == 'GET':
       return render_template('login.html')


def pw_encrypt(pw):
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def pw_valid(pw, stored_hash):
    return pw_encrypt(pw) == stored_hash

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/blog', methods=['GET'])
def blog():
    id = request.args.get('id')
    if id == None:
        return render_template('blogs.html',blogs=Blog.query.all())
    else:
        return render_template('blog.html',blog=Blog.query.filter_by(id=id).first())
@app.route('/', methods=['POST', 'GET'])
def index():
    #$return  encoded_error = request.args.get("error")
    return redirect('/blog')
    

if __name__ == '__main__':
    app.run()