from sanic import Blueprint

from .account.login import bp as login_blueprint
from .account.register import bp as register_blueprint
from .account.password_reset import bp as password_reset_blueprint

from .categories.categories import bp as categories_blueprint
from .transactions.transactions import bp as transactions_blueprint

api_v1 = Blueprint.group(
    login_blueprint,
    register_blueprint,
    password_reset_blueprint,
    categories_blueprint,
    transactions_blueprint,
    url_prefix='/'
)
