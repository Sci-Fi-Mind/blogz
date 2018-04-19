from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Miriam2016@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        
def get_current_blog_list():
    return Blog.query.all()

@app.route('/', methods=['GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def display_blog():
    encoded_id = request.args.get("id")
    if encoded_id:
        post=Blog.query.filter_by(id=encoded_id).first()
        blog_title=post.title
        body=post.body
        return render_template('individual_post.html',title="Post",blog_title=blog_title,body=body)
    else:
        return render_template('blog.html',title="Posts",posts=get_current_blog_list())

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():

    if request.method =='POST':
        new_title = request.form['title']
        new_body = request.form['body']
        title_error=''
        body_error=''
        if new_title == '':
            title_error = "title_error=You forgot to add a title to your post"
            #return redirect("/newpost?title_error=" + title_error)
        if new_body =='':
            body_error = "body_error=You forgot to add text to the body of your post"
            #return redirect("/newpost?body_error=" + body_error)
        if title_error or body_error:
            return redirect("/newpost?"+ title_error + "&" + body_error)
        else:
            new_post = Blog(new_title,new_body)
            db.session.add(new_post)
            db.session.commit()
            new_post_number= str(new_post.id)
            return redirect("/blog?id=" + new_post_number)
    else:
        encoded_title_error = request.args.get("title_error")
        encoded_body_error = request.args.get("body_error")
        return render_template('new_post.html',title="New Post",title_error=encoded_title_error,body_error=encoded_body_error)

if __name__ == '__main__':
    app.run()