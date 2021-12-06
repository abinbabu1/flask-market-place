from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, ValidationError, IntegerField
from wtforms.validators import Email, EqualTo, DataRequired, Length
from .models import User, Item


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'password_conf', message='Passwords should match')])
    password_conf = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):

        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been already registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):

        if not User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Invalid email!')


class ItemForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    barcode = StringField('Barcode', validators=[DataRequired(),
                                                 Length(min=12, max=12, message='Twelve characters required')])
    price = IntegerField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_barcode(self, barcode):

        if Item.query.filter_by(barcode=self.barcode.data).first():
            raise ValidationError('Barcode already exists!')
