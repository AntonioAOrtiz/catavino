import flask_praetorian
from flask import request, jsonify
from flask_restx import abort, Resource, Namespace

from sqlalchemy.sql import text
from model import Post, PostSchema, db

# namespace declaration
api_post = Namespace("posts", "posts management")


@api_post.route("/<post_id>")
class postController(Resource):
    # methods for http methods supported
    # auth required
    @flask_praetorian.auth_required
    def get(self, post_id):
        # gets one user by id
        post = Post.query.get_or_404(post_id)
        # UserSchema() is an object used for ORM objects serialization
        return PostSchema().dump(post)

    # roles required (if several roles, user must have every role)
    @flask_praetorian.roles_required("admin","user")
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        # delete user
        db.session.delete(post)
        # commit needed after every writing operation (not query)
        db.session.commit()
        # using 204 response code
        return f"Deleted post {post_id}", 204

    @flask_praetorian.roles_required("admin","user")
    def put(self, post_id):
        # create User instance from json data located in request body
        new_post = PostSchema().load(request.json)
        # test id mismatch
        if str(new_post.id) != post_id:
            abort(400, "id mismatch")
        # just creating the User instance, data is saved with commit
        db.session.commit()
        # return serialized user using 200 response code
        return PostSchema().dump(new_post)


@api_post.route("/")
class postListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return PostSchema(many=True).dump(Post.query.all())

    @flask_praetorian.roles_required("admin","user")
    def post(self):
        post = PostSchema().load(request.json)
        # add new user
        db.session.add(post)
        db.session.commit()
        return PostSchema().dump(post), 201


