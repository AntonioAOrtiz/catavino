import flask_praetorian
from flask import request, jsonify
from flask_restx import abort, Resource, Namespace

from sqlalchemy.sql import text
from model import Points, PointsSchema, db

# namespace declaration
api_points = Namespace("Points", "Points management")


@api_points.route("/<points_id>")
class PointsController(Resource):
    # methods for http methods supported
    # auth required
    @flask_praetorian.auth_required
    def get(self, Points_id):
        # gets one user by id
        points = Points.query.get_or_404(Points_id)
        # UserSchema() is an object used for ORM objects serialization
        return PointsSchema().dump(points)

    # roles required (if several roles, user must have every role)
    @flask_praetorian.roles_required("admin","user")
    def delete(self, Points_id):
        points = Points.query.get_or_404(Points_id)
        # delete user
        db.session.delete(points)
        # commit needed after every writing operation (not query)
        db.session.commit()
        # using 204 response code
        return f"Deleted Points {Points_id}", 204

    @flask_praetorian.roles_required("admin","user")
    def put(self, Points_id):
        # create User instance from json data located in request body
        new_Points = PointsSchema().load(request.json)
        # test id mismatch
        if str(new_Points.id) != Points_id:
            abort(400, "id mismatch")
        # just creating the User instance, data is saved with commit
        db.session.commit()
        # return serialized user using 200 response code
        return PointsSchema().dump(new_Points)


@api_points.route("/")
class PointsListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return PointsSchema(many=True).dump(Points.query.all())

    @flask_praetorian.roles_required("admin","user")
    def post(self):
        points = PointsSchema().load(request.json)
        # add new user
        db.session.add(Points)
        db.session.commit()
        return PointsSchema().dump(points), 201

