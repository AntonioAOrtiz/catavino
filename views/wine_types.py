import flask_praetorian
from flask import request, jsonify
from flask_restx import abort, Resource, Namespace

from sqlalchemy.sql import text
from model import Wine_type, Wine_typeSchema, db

# namespace declaration
api_wine_type = Namespace("Wine_types", "Wine_types management")


@api_wine_type.route("/<wine_type_id>")
class Wine_typeController(Resource):
    # methods for http methods supported
    # auth required
    @flask_praetorian.auth_required
    def get(self, wine_type_id):
        # gets one user by id
        wine_type = Wine_type.query.get_or_404(wine_type_id)
        # UserSchema() is an object used for ORM objects serialization
        return Wine_typeSchema().dump(wine_type)

    # roles required (if several roles, user must have every role)
    @flask_praetorian.roles_required("admin","user")
    def delete(self, wine_type_id):
        wine_type = Wine_type.query.get_or_404(wine_type_id)
        # delete user
        db.session.delete(wine_type)
        # commit needed after every writing operation (not query)
        db.session.commit()
        # using 204 response code
        return f"Deleted wine_type {wine_type_id}", 204

    @flask_praetorian.roles_required("admin","user")
    def put(self, wine_type_id):
        # create User instance from json data located in request body
        new_wine_type = Wine_typeSchema().load(request.json)
        # test id mismatch
        if str(new_wine_type.id) != wine_type_id:
            abort(400, "id mismatch")
        # just creating the User instance, data is saved with commit
        db.session.commit()
        # return serialized user using 200 response code
        return Wine_typeSchema().dump(new_wine_type)


@api_wine_type.route("/")
class Wyne_typeListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return Wine_typeSchema(many=True).dump(Wine_type.query.all())

    @flask_praetorian.roles_required("admin","user")
    def post(self):
        wine = Wine_typeSchema().load(request.json)
        # add new user
        db.session.add(wine)
        db.session.commit()
        return Wine_typeSchema().dump(wine), 201


