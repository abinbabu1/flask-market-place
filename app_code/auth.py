from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from .forms import LoginForm, SignUpForm
from .models import User
from app_code import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Login Success!")
            return redirect(url_for('views.home'))
        else:
            flash("The password you entered is wrong!")
            return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignUpForm()

    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Signup Successful!")
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)
