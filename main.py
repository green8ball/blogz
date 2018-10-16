from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:mypassword@localhost:8889/blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog %r>' % self.title

# @app.route('/newpost', methods=['GET'])
# def newpost():
    
@app.route('/', methods=['POST', 'GET'])
def index():
    #$return  encoded_error = request.args.get("error")
    return render_template('base.html',)

if __name__ == '__main__':
    app.run()