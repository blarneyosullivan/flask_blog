from flask_blog import app
from flask import render_template, redirect, flash, url_for, session, abort
from blog.form import SetupForm, PostForm
from flask_blog import db
from author.models import Author
from blog.models import Blog, Post, Category
from author.decorators import login_required, author_required
import bcrypt
from slugify import slugify

@app.route('/')
@app.route('/index')
def index():
    blog = Blog.query.first()
    if not blog:
        return redirect(url_for('setup'))
    posts = Post.query.order_by(Post.publish_date.desc())
    return render_template('blog/index.html', blog=blog,  posts=posts)
    #return "hello world!"
    
@app.route('/admin')
# our own decorator
@login_required
@author_required
def admin():
    if session.get('is_author'):
        # get all posts
        #import pdb; pdb.set_trace()
        
        posts = Post.query.order_by(Post.publish_date.desc())
        
        return render_template('blog/admin.html', posts=posts)
    else:
        abort(403)
        
def admin2():
    posts = Post.query.order_by(Post.publish_date.desc())
    return render_template('blog/admin.html', posts=posts)
        
       
@app.route('/setup', methods=('GET', 'POST'))
def setup():
    form = SetupForm()
    error = ""
    
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            True
            )
        db.session.add(author)
        # this will flush data, but not commit, and this gives us an author.id
        db.session.flush()
        if author.id:
            # have author id, so record does not already exit in author table
            # now build blog record
            blog = Blog(
                form.name.data,
                author.id
                )
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback()
            error = "Error creating user"
        
        if author.id and blog.id:
            db.session.commit()
            flash("Blog created")
            return redirect(url_for('admin'))
        else:
            db.session.rollback()
            error = "Error creating blog"
            
    return render_template('blog/setup.html', form=form, error=error)
    
@app.route('/post', methods=('GET', 'POST'))
@author_required
def post():
    #return 'Blog post'
    form = PostForm()
    error = ""
    
    if form.validate_on_submit():
        if form.new_category.data:
            # add new category to database
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        elif form.category.data:
            category_id = form.category.get_pk(form.category.data) # get primary key for form category field
            category = Category.query.filter_by(id=category_id).first()
        else:
            category = None
            
        blog = Blog.query.first() # this app has only 1 blog
        
        author = Author.query.filter_by(username = session['username']).first()
        
        title = form.title.data
        body = form.body.data
        slug = slugify(title)
        
        post = Post(blog, author, title, body,category, slug)
            
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('article', slug=slug))
        
        
    return render_template('blog/post.html', form=form, error=error)

@app.route('/article/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/article.html', post=post)
    
    
    
    