from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
LIMIT = 10


class Posts(db.Model):
    """ Represents blog post

    :id           Int:              post's id
    :title        String:           post's title
    :label        String:           post's label
    :url          String:           post's url
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    label = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(2000), nullable=False)

    def __init__(self, title, label, url):
        self.title = title
        self.label = label
        self.url = url

    def __repr__(self):
        return "<Post #{0}: {1}>".format(self.id, self.title)


@app.route("/")
@app.route("/<label>")
def index(label="Python"):
    posts = Posts.query.filter_by(label=label).limit(LIMIT).all()
    return render_template("index.html", label=label, posts=posts)
