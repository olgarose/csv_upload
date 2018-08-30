import re
from app import db
ALLOWED_EXTENSIONS = {'txt', 'csv'}


def valid_row(row):
    return row[0] and row[1] and row[2]


def valid_header(row):
    return row[0].lower() == 'parent' and row[1].lower() == 'child' and row[2].lower() == 'quantity'


def import_csv(lines, user_id):
    edges = db.metadata.tables['edge']
    connection = db.engine.connect()

    #TODO: Update if exists
    for i, line in enumerate(lines):
        row = line.strip().split(',')
        insert = edges.insert().values(
            parent=row[0],
            child=row[1],
            quantity=row[2],
            user_id=user_id
        )
        connection.execute(insert)
    connection.close()


def valid_rows(lines):
    for i, line in enumerate(lines):
        row = line.strip().split(',')
        if i == 0 and not valid_header(row) or i != 0 and not valid_row(row):
            return False
    return True


def valid_filename(f):
    return '.' in f.filename and f.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


username_regex = re.compile("^[a-zA-Z]+[a-zA-Z0-9_]{2,}$")

USERNAME_RULES = ('Username must contain only letters, numbers, and underscores, must start with a letter and be at '
                  'least 3 characters long.')


def valid_username(username):
    """Validate the username.
    :param username: The user name.
    :raises ValueError: If validation fails.
    """
    if not username_regex.match(username):
        raise ValueError(USERNAME_RULES)
