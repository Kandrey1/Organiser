from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import update, not_, delete
from ..models import db, User, TodoList, ShopList
from ..user.utils import get_all_friends

todo_bp = Blueprint('todo', __name__)


@todo_bp.route("/")
def todo():
    """ Представления главной страницы модуля TODO """
    context = dict()
    context['title'] = 'Модуль "TODO"'
    return render_template("todo/todo.html", context=context)


@todo_bp.route("/shop_list", methods=['GET', 'POST'])
@login_required
def shop_list():
    """ Представления для списка покупок """
    context = dict()
    try:
        context['title'] = 'Список покупок'
        context['shop'] = ShopList.query.filter(
            ShopList.user_id == current_user.id).all()

        if request.method == "POST":
            if "shop_add" in request.form:
                new_shop = request.form.get('shop')
                if new_shop.strip() != "":
                    shop = ShopList(name=new_shop,
                                    check=False,
                                    user_id=current_user.id)
                    db.session.add(shop)
                    db.session.commit()
                    return redirect(url_for('todo.shop_list'))

            if "shop_reset" in request.form:
                db.session.execute(update(ShopList).
                                   where(ShopList.user_id == current_user.id).
                                   values(status_boss=False))
                db.session.commit()

            if "shop_save" in request.form:
                list_check = request.form.getlist('checkedbox')
                db.session.execute(update(ShopList).
                                   where(ShopList.id.in_(list_check)).
                                   values(status_boss=True))
                db.session.execute(update(ShopList).
                                   where(not_(ShopList.id.in_(list_check))).
                                   values(status_boss=False))
                db.session.commit()

            if "shop_delete" in request.form:
                list_del = request.form.getlist('checkedbox')
                db.session.execute(delete(ShopList).
                                   where(ShopList.id.in_(list_del)))
                db.session.commit()
                return redirect(url_for('todo.shop_list'))

    except Exception as e:
        flash(f'Error. <{e}>')

    return render_template("todo/shop_list.html", context=context)


@todo_bp.route("/todo_list", methods=['GET', 'POST'])
@login_required
def todo_list():
    """ Представления для списка дел """
    context = dict()
    try:
        context['title'] = 'Список дел'
        context['todo_user'] = TodoList.query.filter(
            TodoList.worker_id == current_user.id).all()
        context['todo_delegate'] = TodoList.query.filter(
            TodoList.boss_id == current_user.id,
            TodoList.worker_id != current_user.id).join(User).all()

        if request.method == "POST":
            if "todo_add" in request.form:
                new_todo = request.form.get('todo')
                if new_todo.strip() != "":
                    todo = TodoList(name=new_todo,
                                    boss_id=current_user.id,
                                    status_boss=False,
                                    worker_id=current_user.id,
                                    status_worker=False)
                    db.session.add(todo)
                    db.session.commit()
                    return redirect(url_for('todo.todo_list'))

            if "todo_reset" in request.form:
                db.session.execute(update(TodoList).
                                   where(TodoList.boss_id == current_user.id).
                                   values(status_boss=False))
                db.session.commit()

            if "todo_save" in request.form:
                list_check = request.form.getlist('checkedbox')
                db.session.execute(update(TodoList).
                                   where(TodoList.id.in_(list_check)).
                                   values(status_boss=True))
                db.session.execute(update(TodoList).
                                   where(not_(TodoList.id.in_(list_check))).
                                   values(status_boss=False))
                db.session.commit()

            if "todo_delete" in request.form:
                list_del = request.form.getlist('checkedbox')
                db.session.execute(delete(TodoList).
                                   where(TodoList.id.in_(list_del)))
                db.session.commit()
                return redirect(url_for('todo.todo_list'))

            if "todo_delegate" in request.form:
                return redirect(url_for('todo.todo_list_delegate'))
    except Exception as e:
        flash(f'Error. <{e}>')

    return render_template("todo/todo_list.html", context=context)


@todo_bp.route("/todo_list_delegate", methods=['GET', 'POST'])
@login_required
def todo_list_delegate():
    """ Представления для делегирования задач """
    context = dict()
    try:
        context['title'] = 'Делегирование задач'
        context['friends'] = User.query.filter(User.id.in_(get_all_friends())).all()

        todos = TodoList.query.filter(TodoList.boss_id == current_user.id).all()
        context['todos'] = todos

        if "delegate" in request.form:
            todo_id = int(request.form.get('delegate'))
            worker_id = int(request.form.get(f'case_friends-{todo_id}'))
            db.session.execute(update(TodoList).
                               where(TodoList.id == todo_id).
                               values(worker_id=worker_id))
            db.session.commit()
            return redirect(url_for('todo.todo_list'))
    except Exception as e:
        flash(f'Error. <{e}>')

    return render_template("todo/todo_list_delegate.html", context=context)
