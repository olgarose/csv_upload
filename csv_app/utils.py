import re
from csv_app import db
from flask_login import current_user
from sqlalchemy import and_

ALLOWED_EXTENSIONS = {'txt', 'csv'}


def valid_row(row):
    return row[0] and row[1] and row[2]


def valid_header(row):
    return row[0].lower() == 'parent' and row[1].lower() == 'child' and row[2].lower() == 'quantity'


def import_csv(lines):
    connection = db.engine.connect()

    for line in lines:
        row = line.strip().split(',')
        parent, child, quantity = row[0], row[1], row[2]
        cmd = update_edge(parent, child, quantity) if edge_exists(parent, child) else insert_edge(parent, child, quantity)
        connection.execute(cmd)

    connection.close()


def insert_edge(parent, child, quantity):
    edges = db.metadata.tables['edge']
    return edges.insert().values(
        parent=parent,
        child=child,
        quantity=quantity,
        user_id=current_user.get_id()
    )


def update_edge(parent, child, quantity):
    edges = db.metadata.tables['edge']
    return edges.update().values(
        quantity=quantity). \
        where(and_(
        edges.c.parent == parent,
        edges.c.child == child))


def edge_exists(parent, child):
    edges = db.metadata.tables['edge']
    connection = db.engine.connect()
    query = edges.select().where(and_(
        edges.c.parent == parent,
        edges.c.child == child))
    result = connection.execute(query)
    connection.close()
    return result.first()


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
