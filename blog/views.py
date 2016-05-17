from flask_blog import app
from flask import render_template, redirect, flash, url_for, session, abort, request
from blog.form import SetupForm, PostForm
from flask_blog import db, uploaded_images
from author.models import Author
from blog.models import Blog, Post, Category
from author.decorators import login_required, author_required
import bcrypt
from slugify import slugify

# paging
POSTS_PER_PAGE = 5

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    blog = Blog.query.first()
    if not blog:
        return redirect(url_for('setup'))
    # if no page passed then false at end
    posts = Post.query.filter_by(live = True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/index.html', blog=blog,  posts=posts)
    #return "hello world!"
    
@app.route('/admin')
@app.route('/admin/<int:page>')
# our own decorator
@login_required
@author_required
def admin(page=1):
    if session.get('is_author'):
        # get all posts
        #import pdb; pdb.set_trace()
        
        posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
        
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
        image = request.files.get('image')
        filename = None
        try:
            filename = uploaded_images.save(image)
        except:
            flash('The image was not uploaded')
            
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
        
        post = Post(blog, author, title, body,category, filename, slug)
            
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('article', slug=slug))
        
        
    return render_template('blog/post.html', form=form, error=error, action="new")

@app.route('/article/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/article.html', post=post)
    
    
    
@app.route('/delete/<int:post_id>')
@author_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash("Article deleted")
    return redirect('/admin')
    
    
@app.route('/edit/<int:post_id>', methods=('GET','POST'))
@author_required
def edit(post_id):
    # get record
    post = Post.query.filter_by(id=post_id).first_or_404()
    # populate form fields with record data
    form = PostForm(obj=post)
    # form validated
    if form.validate_on_submit():
        # save image
        orig_image = post.image
        # repopulate from form fields
        form.populate_obj(post)
        
        # if form has new image
        if form.image.has_file():
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("the image not uploaded")
            if filename:
                post.image = filename
        else:
            post.image = orig_image
            
        if form.new_category.data:
            new_cat = Category(form.new_category.data)
            db.session.add(new_cat)
            # write new category to get id
            db.session.flush()
            post.category = new_cat
        
        # write full record to database
        db.session.commit()
        
        return redirect(url_for('article', slug=post.slug))
                
            
            
    return render_template('blog/post.html', form=form, post=post, action="edit")
    
