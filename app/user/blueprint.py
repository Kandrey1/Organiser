from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import delete
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import db, User, UserFriend
from .utils import get_all_friends

user_bp = Blueprint('user', __name__)


@user_bp.route("/")
def user():
    """ Представления для главной страницы модуля """
    context = dict()
    context['title'] = 'Модуль "Пользователи"'
    return render_template("user/user.html", context=context)


@user_bp.route("/registration", methods=['GET', 'POST'])
def registration():
    """ Представления для страницы регистрации нового пользователя """
    context = dict()
    try:
        context['title'] = 'Регистрация'
        if request.method == "POST":
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()

            pass_hash = generate_password_hash(password, method='sha256')

            if user:
                flash('Пользователь с таким email уже существует')
                return redirect(url_for('user.registration'))

            new_user = User(name=name, email=email, password=pass_hash)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('user.profile'))

    except Exception as e:
        flash(f'Error. <{e}>')

    return render_template("user/registration.html", context=context)


@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    """ Представления для страницы авторизации """
    context = dict()
    try:
        context['title'] = 'Авторизация'

        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password, password):
                flash('Неверный логин или пароль')
                return redirect(url_for('user.login'))

            login_user(user)

            return redirect(url_for('user.profile'))

    except Exception as e:
        flash(f'Error. <{e}>')

    return render_template("user/login.html", context=context)


@user_bp.route("/logout")
@login_required
def logout():
    """ Представления для logout """
    logout_user()
    return redirect(url_for('user.login'))


@user_bp.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    """ Представления для личного кабинете """
    context = dict()
    try:
        context['title'] = 'Личный кабинет'
        context['friends'] = User.query.filter(User.id.in_(get_all_friends())).all()

        if request.method == "POST":
            if "find__user" in request.form:
                name = request.form.get('name')
                users = User.query.filter(User.name.like(f'%{name}%')).all()
                context['users'] = users

            if "case__friend" in request.form:
                friend_id = request.form.get('radio')
                friend = UserFriend(friend_one=current_user.id,
                                    friend_two=friend_id)
                db.session.add(friend)
                db.session.commit()
                return redirect(url_for('user.profile'))

            if "delete__friend" in request.form:
                del_id_friend = request.form.get('delete__friend')
                db.session.execute(delete(UserFriend).
                                where((UserFriend.friend_one == current_user.id) &
                                      (UserFriend.friend_two == del_id_friend)))
                db.session.commit()
                return redirect(url_for('user.profile'))
    except Exception as e:
        flash(f'Error. <{e}>')

    return render_template("user/profile.html", context=context)
