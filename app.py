from flask import Flask, jsonify, request, url_for
from authlib.integrations.flask_client import OAuth
import flask_praetorian

from model import init_db, User


# import blueprint
from views import blueprint as api


def create_app(config_file='config.py'):
    # instantiate praetorian object
    guard = flask_praetorian.Praetorian()
    # TODO: cors config

    # instantiate flask app
    app = Flask(__name__)

    # get configuration parameters
    # TODO: initial config for tests
    app.config.from_pyfile(config_file)

    # instantiate oauth object
    oauth = OAuth(app)

    # oauth init
    oauth.register(
        name='github',
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )

    # praetorian init
    guard.init_app(app, User)

    # SQLAlchemy init
    init_db(app, guard, 'tests' in config_file)

    # register blueprint
    app.register_blueprint(api, url_prefix="/api/")


    @app.route("/")
    def home():
        """
        Home page

        Send static file with link to api to avoid 404 on /
        """
        return app.send_static_file("index.html")


    # authentication system
    @app.route('/login', methods=['POST'])
    def login():
        """
        Process login requests

        Get login credentials from body using json
        Parameters: username and password
        """
        # get username and password from body (json)
        username = request.json.get('username')
        password = request.json.get('password')
        # praetorian authentication
        user = guard.authenticate(username, password)
        # get JWT from praetorian
        ret = {"access_token": guard.encode_jwt_token(user)}
        # return JWT
        return jsonify(ret), 200


    @app.route('/github')
    def oauth_login():
        """
        Send gitHub authorization request

        Creates Authlib client for OAuth with gitHub
        """

        # create auth client for gitHub
        github = oauth.create_client('github')
        # _external=True because gitHub redirects to this url
        redirect_uri = url_for('authorize', _external=True)
        # send authorization request
        return github.authorize_redirect(redirect_uri)


    @app.route('/authorize')
    def authorize():
        """
        Process gitHub authorization

        Redirect Uri for gitHub OAuth authorization
        """

        # get token for gitHub API access
        token = oauth.github.authorize_access_token()
        # /user gitHub API entrypoint ()
        resp = oauth.github.get('user', token=token)
        resp.raise_for_status()
        # get json from API response
        profile = resp.json()

        # TODO: add user when new email

        # bad code: updating password on fly
        # user_github = User.query.filter_by(username=profile.get("login")).first()
        # user_github.hashed_password = guard.hash_password(token.get("access_token"))
        # db.session.commit()
        # db.session.close()

        # get user using gitHub username
        user = User.lookup(profile.get("login"))
        # get JWT from praetorian
        ret = {"access_token": guard.encode_jwt_token(user)}
        # return JWT
        return jsonify(ret), 200
    return app


if __name__ == '__main__':
    # starts app
    # in production: debug=False
    app = create_app()
    app.run(debug=True)
