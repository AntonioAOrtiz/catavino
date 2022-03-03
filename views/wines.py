import flask_praetorian
from flask import request, jsonify
from flask_restx import abort, Resource, Namespace

from sqlalchemy.sql import text
from model import Wine, WineSchema, db

# namespace declaration
api_wine = Namespace("Wines", "Wines management")


@api_wine.route("/<wine_id>")
class WineController(Resource):
    # methods for http methods supported
    # auth required
    @flask_praetorian.auth_required
    def get(self, wine_id):
        # gets one user by id
        wine = Wine.query.get_or_404(wine_id)
        # UserSchema() is an object used for ORM objects serialization
        return WineSchema().dump(wine)

    # roles required (if several roles, user must have every role)
    @flask_praetorian.roles_required("admin","user")
    def delete(self, wine_id):
        wine = Wine.query.get_or_404(wine_id)
        # delete user
        db.session.delete(wine)
        # commit needed after every writing operation (not query)
        db.session.commit()
        # using 204 response code
        return f"Deleted wine {wine_id}", 204

    @flask_praetorian.roles_required("admin","user")
    def put(self, wine_id):
        # create User instance from json data located in request body
        new_wine = WineSchema().load(request.json)
        # test id mismatch
        if str(new_wine.id) != wine_id:
            abort(400, "id mismatch")
        # just creating the User instance, data is saved with commit
        db.session.commit()
        # return serialized user using 200 response code
        return WineSchema().dump(new_wine)


@api_wine.route("/")
class WineListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return WineSchema(many=True).dump(Wine.query.all())

    @flask_praetorian.roles_required("admin","user")
    def post(self):
        wine = WineSchema().load(request.json)
        # add new user
        db.session.add(wine)
        db.session.commit()
        return WineSchema().dump(wine), 201


@api_wine.route("/wine_points")
class WinePointsListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        # using custom SQL
        statement = text("""
            select wine.name as name, avg(points.points) as avg
            from wine join on points.wine_id = wine.id
            group by wine.id
            """)
        result = db.session.execute(statement)
        return jsonify({r['name']: r['avg'] for r in result})
