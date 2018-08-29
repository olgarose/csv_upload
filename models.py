from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField,  BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import lazy_gettext as _

from csv_utils.utils import USERNAME_RULES, valid_username

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "User"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(300))


def strip_filter(text):
    return text.strip() if text else text


class LoginForm(FlaskForm):
    username = StringField(
        label=_('Username'),
        validators=[DataRequired(message=_('Username not provided.'))],
        filters=[strip_filter],)

    password = PasswordField(
        label=_('Password'),
        validators=[DataRequired(message=_('Password not provided.'))],)

    remember_me = BooleanField(_('Remember Me'))


class RegistrationForm(FlaskForm):
    username = StringField(
        label=_('Username'),
        description=_('Required. %(username_rules)s',
                      username_rules=USERNAME_RULES),
        validators=[DataRequired(message=_('Username not provided.'))],
        filters=[strip_filter],
    )

    email = StringField(
        label=_('Email'),
        validators=[DataRequired(message=_('Email not provided.')), Email()]
    )

    password = PasswordField(
        label=_('Password'),
        validators=[DataRequired(message=_('Password not provided.'))],)

    password2 = PasswordField(
        label=_('Confirm Password'),
        validators=[DataRequired(message=_('Must confirm password.')),
                    EqualTo('password')])

    def validate_username(self, username):
        try:
            valid_username(username.data)
        except ValueError:
            raise ValidationError('Invalid Username')

        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address already registered.')


