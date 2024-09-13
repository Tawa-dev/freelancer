from flask import redirect, render_template, url_for, flash, request, Blueprint, session
from flask_login import login_user, current_user, logout_user
from banc import db
from werkzeug.security import generate_password_hash, check_password_hash
from banc.models import User, Skills
from banc.users.forms import RegistrationForm, LoginForm
from datetime import datetime
import os
import secrets
from PIL import Image
from flask import current_app

# function to save uploaded files to file system
def save_picture(form_picture):
    # generate a random set of characters
    random_hex = secrets.token_hex(8)
    # save the given file extension to f_ext
    _,f_ext = os.path.splitext(form_picture.filename)
    # combine the random set of characters and the file extension to create a new name for the  file
    picture_fn = random_hex + f_ext
    # create the path were file will be saved
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    # save file to specified path
    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn

users = Blueprint('users',__name__)

@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('users.register'))
    form = RegistrationForm()
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'])
        user = User(email=request.form['email'],password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created, you are now able to login!','success')
        return redirect(url_for('users.profile'))
    return render_template('signup.html',form=form)

@users.route('/', methods=['GET','POST'])
@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('users.login'))
    form = LoginForm()
    if request.method =='POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password,request.form['password']):
            login_user(user, remember=request.form['remember'])
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.browse'))
        else:    
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('index.html',form=form)

# route that returns the profile setup page after sign up
@users.route('/profile', methods=['GET','POST'])
def profile():
    if request.method == 'POST':
        #  configure today date
        todayDate = str(datetime.today().date())
        currentTime = str(datetime.now().time())
        dateJoinedStr = todayDate + currentTime
        dateJoinedObj = datetime.strptime(dateJoinedStr[0:18], '%Y-%m-%d%H:%M:%S')
        #fetch user with email that just signed up and update the details
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.username = request.form['username']
            user.image_file = save_picture(request.files['image_file'])
            user.fullname = request.form['fullname']
            user.profession = request.form['profession']
            user.description = request.form['description']
            user.languages = request.form['languages']
            user.home_address = request.form['home_address']
            user.rate = request.form['rate']
            user.date_joined = dateJoinedObj
            #get list of skills from input fields which have been dynamically created in javascript 
            #add each skill to Skills database
            for skill in request.form:
                if skill[0:5] == 'skill':
                    sk = Skills(skill_name=request.form[skill],user_id=current_user.id)
                    db.session.add(sk)
            db.session.commit()
            return redirect(url_for('main.browse'))

    return render_template('profile.html')

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login')) 