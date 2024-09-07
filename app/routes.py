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

from flask import Flask, request, redirect, url_for, flash, render_template
import os
from flask_login import login_required

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
@login_required  # This will ensure the user is logged in before uploading
def upload():
    if request.method == 'POST':  # Handle file upload when form is submitted
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)  # Stay on the same page to show error message

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty part without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)  # Stay on the same page if no file is selected

        if file:
            # Ensure the uploads directory exists
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            # Save the file
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            
            # After successfully saving, redirect to visualization page
            flash('File successfully uploaded')
            return redirect(url_for('visualization'))

        flash('File upload failed')
        return redirect(url_for('upload'))  # In case something else goes wrong

    # Render the upload form (for GET requests)
    return render_template('upload.html')



@app.route("/visualization/<filename>")
@login_required
def visualization(filename):
    data = pd.read_csv(filename)
    return render_template('visualization.html', title='Data Visualization', data=data.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)