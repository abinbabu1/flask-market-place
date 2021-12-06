from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user, login_required
from app_code import db

from .forms import ItemForm
from .models import Item, User

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')


@views.route('/market')
def market_page():
    # items = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    # ]
    items = Item.query.all()
    return render_template('market.html', items=items)


@views.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():

    form = ItemForm()

    if form.validate_on_submit():
        item = Item(name=form.name.data,
                    barcode=form.barcode.data,
                    price=form.price.data,
                    description=form.description.data,
                    owner_id=current_user.id)
        db.session.add(item)
        db.session.commit()

        return redirect(url_for('views.user_items'))
    return render_template('add_item.html', form=form)


@views.route('user_items')
@login_required
def user_items():
    items = Item.query.filter_by(owner=current_user).all()
    return render_template('user_items.html', items=items)
