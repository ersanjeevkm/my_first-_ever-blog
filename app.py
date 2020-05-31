from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"

db = SQLAlchemy(app)

class Blogposts(db.Model):
    id = db.Column(db.Integer,primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(30), nullable=False, default='Anonymous')
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now().replace(microsecond=0))

@app.route('/')
def welcome():
    return render_template("home.html")

@app.route('/posts')
def posts():
    blog_posts = Blogposts.query.order_by(Blogposts.date_posted.desc()).all()
    return render_template("posts.html", posts = blog_posts)

@app.route("/posts/new",methods=["GET","POST"])
def new_post():
    if(request.method == "POST"):
        if request.form['author']:
            post_auth = request.form['author']
        post_title = request.form['title']
        post_content = request.form['content']

        if request.form['author']:
            newpost = Blogposts(title=post_title,author=post_auth,content=post_content)
        else:
            newpost = Blogposts(title=post_title, content=post_content)
        db.session.add(newpost)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("new_post.html")

@app.route("/posts/delete/<int:id>")
def del_post(id):
    post = Blogposts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")

@app.route("/posts/edit/<int:id>",methods=["GET","POST"])
def edit_post(id):
    editpost = Blogposts.query.get_or_404(id)
    if request.method == "POST":
        editpost.title = request.form["title"]
        editpost.author = request.form["author"]
        editpost.content = request.form["content"]
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template("post_edit.html", post = editpost)

if __name__ == '__main__':
    app.run(debug=True)
