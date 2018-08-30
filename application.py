from flask import render_template, request, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect
from werkzeug.urls import url_parse

from csv_app.utils import valid_filename, valid_rows, import_csv
from csv_app.models import User
from csv_app.forms import LoginForm, RegistrationForm
from csv_app import app, db


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')


@app.route('/message', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        lines = uploaded_file.readlines()
        if valid_filename(uploaded_file) and valid_rows(lines):
            import_csv(lines[1:])
            return render_template('thanks.html')
        else:
            return render_template('error.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run()
