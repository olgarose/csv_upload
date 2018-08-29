from flask import Flask, render_template, request, url_for, g, flash
from flask_login import LoginManager, current_user, login_user, login_required
from werkzeug.utils import redirect

from csv_utils.utils import valid_filename, valid_rows, put_csv
import database as db
from models import User, LoginForm

application = Flask(__name__)
login_manager = LoginManager()

login_manager.init_app(application)
db.init(application)

application.config['SECRET_KEY'] = 'the secretest key'


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/upload')
@login_required
def upload():
    return render_template('upload.html')


@application.route('/message', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        lines = uploaded_file.readlines()
        if valid_filename(uploaded_file) and valid_rows(lines):
            put_csv(lines[1:], db)
            return render_template('thanks.html')
        else:
            return render_template('error.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@application.route('/login', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


if __name__ == '__main__':
    application.run()
