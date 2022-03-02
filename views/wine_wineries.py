import flask_praetorian
from flask import request, jsonify
from flask_restx import abort, Resource, Namespace

from sqlalchemy.sql import text
from model import Wine_winery, Wine_winerySchema, db

# namespace declaration
api_wine_winery = Namespace("Wine_wineries", "Wine_wineries management")


@api_wine_winery.route("/<wine_winery_id>")
class Wine_wineryController(Resource):
    # methods for http methods supported
    # auth required
    @flask_praetorian.auth_required
    def get(self, wine_winery_id):
        # gets one user by id
        wine_winery = Wine_winery.query.get_or_404(wine_winery_id)
        # UserSchema() is an object used for ORM objects serialization
        return Wine_winerySchema().dump(wine_winery)

    # roles required (if several roles, user must have every role)
    @flask_praetorian.roles_required("admin","user")
    def delete(self, wine_winery_id):
        wine_winery = Wine_winery.query.get_or_404(wine_winery_id)
        # delete user
        db.session.delete(wine_winery)
        # commit needed after every writing operation (not query)
        db.session.commit()
        # using 204 response code
        return f"Deleted wine_winery {wine_winery_id}", 204

    @flask_praetorian.roles_required("admin","user")
    def put(self, wine_winery_id):
        # create User instance from json data located in request body
        new_wine_winery = Wine_winerySchema().load(request.json)
        # test id mismatch
        if str(new_wine_winery.id) != wine_winery_id:
            abort(400, "id mismatch")
        # just creating the User instance, data is saved with commit
        db.session.commit()
        # return serialized user using 200 response code
        return Wine_winerySchema().dump(new_wine_winery)


@api_wine_winery.route("/")
class Wyne_wineryListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return Wine_winerySchema(many=True).dump(Wine_winery.query.all())

    @flask_praetorian.roles_required("admin","user")
    def post(self):
        wine = Wine_winerySchema().load(request.json)
        # add new user
        db.session.add(wine)
        db.session.commit()
        return Wine_winerySchema().dump(wine), 201


