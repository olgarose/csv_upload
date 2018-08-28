from sqlalchemy import create_engine
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)


def init(application):
    application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    create_tables()


def create_tables():
    create_user_table()
    create_edge_table()


def create_edge_table():
    execute_command('CREATE TABLE IF NOT EXISTS Edges('
                    'edge_id INTEGER AUTO_INCREMENT NOT NULL, '
                    'parent VARCHAR(255) NOT NULL, '
                    'child VARCHAR(255) NOT NULL,'
                    'quantity INTEGER NOT NULL,'
                    'user_id INTEGER,'
                    'FOREIGN KEY (user_id) REFERENCES Users(user_id) , '
                    'PRIMARY KEY(edge_id)); ')


def create_user_table():
    execute_command('CREATE TABLE IF NOT EXISTS Users('
                    'user_id INTEGER AUTO_INCREMENT NOT NULL, '
                    'email VARCHAR(255),'
                    'PRIMARY KEY(user_id));')


def execute_command(command):
    connection = engine.connect()
    connection.execute(command)
    connection.close()
