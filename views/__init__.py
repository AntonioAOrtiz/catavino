from flask import Blueprint
from flask_restx import Api
import flask_praetorian

from .users import api_user
from .wines import api_wine
from .wine_types import api_wine_type
from .wine_wineries import api_wine_winery
from .posts import api_post
from .points import api_point

# one blueprint (Flask) for all the resources
blueprint = Blueprint('CataVino', __name__)
api = Api(blueprint, title="CataVino", version="1.0", description="", doc="/docs")
flask_praetorian.PraetorianError.register_error_handler_with_flask_restx(api_user)
flask_praetorian.PraetorianError.register_error_handler_with_flask_restx(api_wine)
flask_praetorian.PraetorianError.register_error_handler_with_flask_restx(api_wine_type)
flask_praetorian.PraetorianError.register_error_handler_with_flask_restx(api_wine_winery)
flask_praetorian.PraetorianError.register_error_handler_with_flask_restx(api_post)
flask_praetorian.PraetorianError.register_error_handler_with_flask_restx(api_point)

# every resource in a namespace (RestX)
api.add_namespace(api_user, path='/user')
api.add_namespace(api_wine, path='/wine')
api.add_namespace(api_wine_type, path='/wine_type')
api.add_namespace(api_wine_winery, path='/wine_winery')
api.add_namespace(api_post, path='/post')
api.add_namespace(api_point, path='/point')
