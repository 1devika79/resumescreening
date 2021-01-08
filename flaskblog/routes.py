import os
import secrets
import flask_whooshalchemy as wa
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm,RegistrationFormE, LoginFormE,LoginForm, UpdateAccountForm, PostForm,MultiCheckboxField, SimpleForm
from flaskblog.models import User,Employee, Post,Company
from flask_login import login_user, current_user, logout_user, login_required

from flaskblog.algorithms import recommand,automation
app.config['WHOOSH_BASE']='whoosh'




@app.route("/")
def Welcome():
    return render_template('welcome.html')

@app.route("/home")
def home():
    print(current_user)
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

'''@app.route("/ehome")
def ehome():
    print(current_user)
    posts = Post.query.all()
    users=  Employee.query.all()
    print(users)
    return render_template('ehome.html', posts=posts,user=users)
'''
@app.route("/about")
def about():
    return render_template('about.html', title='About')
@app.route("/eabout")
def eabout():
    return render_template('eabout.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    us="Company"
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        comp = Company(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.add(comp)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form,use=us)


@app.route("/loginC", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    us="Company"
    if form.validate_on_submit():
        user = Company.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            user = User.query.filter_by(email=form.email.data).first()
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form,use=us)


@app.route("/registerE", methods=['GET', 'POST'])
def registerE():
  
    if current_user.is_authenticated and Employee.query.filter_by(email=current_user.email).first():
        return redirect(url_for('ehome'))
        
    form = RegistrationFormE()
    us="Employee"
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        emp = Employee(username=form.username.data, email=form.email.data, password=hashed_password)
       
        db.session.add(user)
        db.session.add(emp)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('loginE'))
    return render_template('register.html', title='Register', form=form,use=us)


@app.route("/loginE", methods=['GET', 'POST'])
def loginE():
    if current_user.is_authenticated and Employee.query.filter_by(email=current_user.email).first():
        return redirect(url_for('ehome'))
    form = LoginFormE()
    us= "Employee"
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            use=User.query.filter_by(email=form.email.data).first()
            login_user(use, remember=form.remember.data)
            next_page = request.args.get('next')
            print(current_user)
            return redirect(next_page) if next_page else redirect(url_for('ehome'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form,use=us)


@app.route("/logout")
def logout(): 
    logout_user()
    return redirect(url_for('Welcome'))


def save_picture(form_picture):
    print(form_picture.filename)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\profile-pics', picture_fn)
    print(picture_path)
    print(picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/search",methods=['GET', 'POST'])
def search():
    print(Post.query.filter(Post.title.contains('h')).all())
    post=Post.query.filter(Post.title.contains(request.args.get('query'))).all() +Post.query.filter(Post.content.contains(request.args.get('query'))).all()
    return render_template('home.html',posts=post)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            print(form.picture.data)
            current_user.image_file = picture_file
        co=Company.query.filter_by(username=current_user.username).first()
        co.username = form.username.data
        co.email = form.email.data
        db.session.commit()
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics' + current_user.image_file)
    print(image_file)
    print('profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/Eaccount", methods=['GET', 'POST'])
@login_required
def Eaccount():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        emp=Employee.query.filter_by(username=current_user.username).first()
        emp.username = form.username.data
        emp.email = form.email.data
        db.session.commit()
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('Eaccount'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics' + current_user.image_file)
    return render_template('Eaccount.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        form1=form.minpro.data+form.mindes.data+form.minsoft.data+form.minmarket.data
        form2=form.maxpro.data+form.maxdes.data+form.maxsoft.data+form.maxmarket.data
        min1=",".join(form1)
        max1=",".join(form2)
        post = Post(title=form.title.data, content=form.content.data, author=current_user,skillsrequired=max1,minskillsrequired=min1,Category=form.Category.data ,Salary=form.salary.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    print(post)
    emp=Employee.query.filter_by(email=current_user.email).first()
    return render_template('post.html', title=post.title, post=post,Emp=emp)

@app.route("/poste/<int:post_id>")
def poste(post_id):
    post = Post.query.get_or_404(post_id)
    print(post)
    emp=Employee.query.filter_by(email=current_user.email).first()
    return render_template('poste.html', title=post.title, post=post,Emp=emp)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        form1=form.minpro.data+form.mindes.data+form.minsoft.data+form.minmarket.data
        form2=form.maxpro.data+form.maxdes.data+form.maxsoft.data+form.maxmarket.data
        min1=",".join(form1)
        max1=",".join(form2)
        if len(min1)!=0:
            post.minskillsrequired=min1
        if len(max1)!=0:
            post.skillsrequired=max1
        post.Category=form.Category.data
        post.title = form.title.data
        post.content = form.content.data
        post.Salary=form.salary.data
        print(form.salary.data)
        print(post.Salary)
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.Category.data=post.Category
        form.salary.data=post.Salary
        
        
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
'''
@app.route("/post/<int:post_id>/generate", methods=['GET', 'POST'])
@login_required
def generate_post(post_id):
    post = Post.query.get_or_404(post_id)
    EP=list(map(int,post.candi_ids.split(',')))
    Emp=[Employee.query.filter_by(id=id).one() for id in EP]
    
    print(Emp)
    #db.session.delete(post)
    #db.session.commit()
    flash('Generation in process', 'success')
    return redirect(url_for('post', post_id=post.id))
'''
@app.route("/post/<int:post_id>/apply", methods=['GET', 'POST'])
@login_required
def apply_post(post_id):
    post = Post.query.get_or_404(post_id)
    emp=Employee.query.filter_by(email=current_user.email).first()
    if post.candi_ids is not None:
        EP=list(map(int,post.candi_ids.split(',')))
        if emp.id in EP:
            flash('Already applied!', 'success')
            return redirect(url_for('poste', post_id=post.id))
    #emp_post=Employee.query.filter_by(EP in candi_ids).first()
    if emp =='':
        abort(403)
    
    if(post.candi_ids is not None and emp.joballot is not None):
        new_candi=post.candi_ids+','+str(emp.id)
        new_joballot=emp.joballot+','+str(post_id)
        print(new_candi)
        print(new_joballot)
    elif(post.candi_ids is None and emp.joballot is not None):
        new_candi=emp.id 
        new_joballot=emp.joballot+','+str(post_id)
        print(new_candi)
        print(new_joballot)
    elif(post.candi_ids is not None and emp.joballot is None):
        new_candi=post.candi_ids+','+str(emp.id)
        new_joballot=post_id
        print(new_candi)
        print(new_joballot)
    else:
        new_candi=emp.id
        new_joballot=post_id
        print(new_candi)
        print(new_joballot)
    post.candi_ids=new_candi
    emp.joballot=new_joballot
    db.session.commit()
    flash('Your post has been updated!', 'success')
    return redirect(url_for('poste', post_id=post.id))

@app.route("/survey",methods=['GET', 'POST'])
def survey():
    
    form=SimpleForm()
    post = Employee.query.filter_by(email=current_user.email).first()
    print(post)
    print(current_user.id)
    if form.validate_on_submit():
        print(type(form.examplelan.data))
        form1=form.examplepro.data+form.exampledes.data+form.examplesoft.data+form.examplemarket.data
        print(current_user.id)
        print(form.address.data)
        print(type(form.address.data))
        s=",".join(form1)
        print(s)
        post.phn_no = form.phn_no.data
        post.address = form.address.data
        post.age = form.age.data
        post.spec = form.spec.data
        post.exp = form.exp.data
        post.gitid = form.gitid.data
        post.linkedin = form.linkedin.data
        post.skills=s
        db.session.commit()
        print(current_user.id)
        flash('Your profile has been Updated!', 'success')
        return redirect(url_for('ehome'))
    else:
        print("ERROR on validation")
        print(request.method)
        print(form.validate_on_submit())
    return render_template('survey.html', title='Survey',
                           form=form, legend='Survey')

@app.route("/post/<int:post_id>/generate", methods=['GET', 'POST'])
@login_required
def generate_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.candi_ids is None:
        flash('No one has applied for the job', 'success')
        return redirect(url_for('post' , post_id=post.id))
    EP=list(map(int,post.candi_ids.split(',')))
    print(EP)
    emp=[Employee.query.filter_by(id=id).one() for id in EP]
    
    print(emp)
    automation(EP,post_id,post)
    #db.session.delete(post)
    #db.session.commit()
    flash('Generation in process', 'success')
    return redirect(url_for('post', post_id=post.id))

@app.route("/ehome")
def ehome():
    print(current_user)
    posts = Post.query.all()
    users=  Employee.query.all()
    emp_id=Employee.query.filter_by(email=current_user.email).first()
    if(emp_id.skills is not None):
        l2=recommand(emp_id.id)
        print(l2)
        recom=[Post.query.filter_by(id=id).one() for id in l2]
        posts=recom
        print(posts)
    return render_template('ehome.html', posts=posts,user=users)

@app.route("/jobs")
def jobs():
    posts = Post.query.all()
    return render_template('jobs.html', posts=posts)
