from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from csv_utils import utils
import database as db

application = Flask(__name__)

db.init(application)


@application.route('/')
def index():
    return redirect(url_for('upload'))


@application.route('/upload')
def upload():
    return render_template('index.html')


@application.route('/message', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        lines = uploaded_file.readlines()
        if utils.valid_name(uploaded_file) and utils.valid_rows(lines):
            utils.put_csv(lines[1:], db)
            return render_template('thanks.html')
        else:
            return render_template('error.html')


if __name__ == '__main__':
    application.run()
