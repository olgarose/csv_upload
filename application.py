from flask import Flask, render_template, request, url_for, g
from werkzeug.utils import redirect

from csv_utils.utils import valid_name, valid_rows, put_csv
import database as db

application = Flask(__name__)
db.init(application)


@application.route('/')
def index():
    return redirect(url_for('upload'))


@application.route('/message', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        lines = uploaded_file.readlines()
        if valid_name(uploaded_file) and valid_rows(lines):
            put_csv(lines[1:], db)
            return render_template('thanks.html')
        else:
            return render_template('error.html')


if __name__ == '__main__':
    application.run()
