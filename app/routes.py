from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UploadForm
from app.models import User, Dataset
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
import os

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.dataset.data
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        data = pd.read_csv(filepath)
        # Perform data sanitization here
        data.dropna(inplace=True)
        sanitized_filepath = os.path.join('uploads', 'sanitized_' + file.filename)
        data.to_csv(sanitized_filepath, index=False)
        dataset = Dataset(name=file.filename, user_id=current_user.id)
        db.session.add(dataset)
        db.session.commit()
        flash('Your file has been uploaded and sanitized!', 'success')
        return redirect(url_for('visualization', filename=sanitized_filepath))
    return render_template('upload.html', title='Upload Data', form=form)

@app.route("/visualization/<filename>")
@login_required
def visualization(filename):
    data = pd.read_csv(filename)
    return render_template('visualization.html', title='Data Visualization', data=data.to_dict(orient='records'))

