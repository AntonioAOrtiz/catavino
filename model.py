from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields
from sqlalchemy import true
from sqlalchemy_utils import database_exists
from flask_restx import fields as restx_fields

db = SQLAlchemy()


def init_db(app, guard, testing=False):
    """
    Initializes database

    :param app: flask app
    :param guard: praetorian object for password hashing if seeding needed
    """
    db.init_app(app)
    if testing or not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        # if there is no database file
        # migrate model
        db.create_all(app=app)
        # seed data
        seed_db(app, guard)


def seed_db(app, guard):
    """
    Seeds database with test data

    :param app: flask app
    :param guard: praetorian object for password hashing
    """
    # when using app var in function, we need to use app_context
    with app.app_context():
        # lists of model objects for db seed
        # commit changes in database
        roles = [
            Role(id = 1,name="admin"),
            Role(id = 2,name="user"),
        ]
        
        users = [
            User(id=1,
            username="ToniCaswepss",
            name="Antonio",
            lastname1="Ortiz",
            lastname2="García",
            email="antonioortiz561@gmail.com",
            password="pestillo",
            roles=roles[0],
            ),
            User(id=2,
            username="Tulkas72",
            name="José Manuel",
            lastname1="Sánchez",
            lastname2="Alvarez",
            email="tulkas72@gmail.com",
            password="pestillo123",
            roles=roles[1],
            )
        ]

        wines = [
            Wine(id = 1,
                name = "Tío Pepe",
                winery = "González Byass",
                appellation_origin = "Jerez, Xérès, Sherry",
                country = "España",
                type = "Espirituoso",
                aging = "Cuatro años",
                grapes = "Palomino Fino",
                alcohol = "15",
                description = "Vino 100% procedente de uva Palomino Fino, de crianza biológica y que como mínimo reposa 4 años en bota de roble americano siguiendo el sistema tradicional de criaderas y solera.",
                price = 6.99
            )]
        
        points = [
            Points(id = 1,
            points = 8,
            user_id = 1,
            wine_id = 1
            ),
            Points(id = 2,
            point = 7.5,
            user_id = 2,
            wine_id = 1
            )
        ]
        
        for rol in roles:
            db.session.add(rol)        
        for user in users:
            db.session.add(user)
        for wine in wines:
            db.session.add(wine)
        for point in points:
            db.session.add(point)
        
        db.session.commit()


# table for N:M relationship
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                       )



# classes for model entities
class User(db.Model):
    """
    User entity
    user data
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    lastname1 = db.Column(db.String(80), unique=True, nullable=False)
    lastname2 = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    

    # from praetorian example
    password = db.Column(db.Text)
    # M:N relationship
    roles = db.relationship('Role', secondary=roles_users)
    is_active = db.Column(db.Boolean, default=True, server_default="true")
    
    wine = db.relationship("Points", backref="user")
    posts = db.relationship('Post', backref='user', lazy=True)

    # this enable this entity as user entity in praetorian
    @property
    def identity(self):
        """
        *Required Attribute or Property*
        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return self.id

    @property
    def rolenames(self):
        """
        *Required Attribute or Property*
        flask-praetorian requires that the user class has a ``rolenames`` instance
        attribute or property that provides a list of strings that describe the roles
        attached to the user instance
        """
        # try:
        #     return self.roles.split(",")
        # except Exception:
        #     return []
        return [role.name for role in self.roles]

    """@property
    def password(self):
        
        *Required Attribute or Property*
        flask-praetorian requires that the user class has a ``password`` instance
        attribute or property that provides the hashed password assigned to the user
        instance
        

        return self.password"""

    @classmethod
    def lookup(cls, username):
        """
        *Required Method*
        flask-praetorian requires that the user class implements a ``lookup()``
        class method that takes a single ``username`` argument and returns a user
        instance if there is one that matches or ``None`` if there is not.
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id_user):
        """
        *Required Method*
        flask-praetorian requires that the user class implements an ``identify()``
        class method that takes a single ``id`` argument and returns user instance if
        there is one that matches or ``None`` if there is not.
        """
        return cls.query.get(id_user)

    def is_valid(self):
        return self.is_active

    # specify string for repr
    def __repr__(self):
        return f"<{self.username}>"


class Role(db.Model):
    """
    Role entity
    roles data
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"<{self.name}>"


class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    winery = db.Column(db.String(80), unique=False, nullable=False)
    appellation_origin = db.Column(db.String(80), unique=False, nullable=True)
    year = db.Column(db.Numeric(4), unique=False, nullable=True)
    country = db.Column(db.String(80), unique=False, nullable=True)
    type = db.Column(db.String(80), unique=False, nullable=False)
    aging = db.Column(db.String(80), unique=False, nullable=True)
    grapes = db.Column(db.String(80), unique=False, nullable=True)
    alcohol = db.Column(db.Numeric(3,1), unique=False, nullable=True)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(8,2), unique=False, nullable=True)
    points = db.Column(db.Numeric(1,1), unique=False, nullable=True)
    
    
    posts = db.relationship('Post', backref='wine', lazy=True)

    
    
    def __repr__(self):
        return f"<{self.name}>"


class Wine_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wine.id'), nullable=False)

    def __repr__(self):
        return f"<{self.name}>"


class Wine_winery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wine.id'), nullable=False)

    def __repr__(self):
        return f"<{self.name}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wine.id'), nullable=False)
    content = db.Column(db.Text)
    publish_date = db.Column(db.DateTime())

    def __repr__(self):
        return f"<{self.content}>"


class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Numeric(1,1), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wine.id'), nullable=False)

    

    def __repr__(self):
        return f"<{self.points}>"


# Marshmallow schemas definition
class SchemaDocSwagger(SQLAlchemyAutoSchema):
    @staticmethod
    def transport_field_class(field, api, nested):
        if "String" in str(type(field)):
            return restx_fields.String
        if "Boolean" in str(type(field)):
            return restx_fields.Boolean
        if nested:
            return restx_fields.Integer
        if "Nested" in str(type(field)):
            return restx_fields.List(restx_fields.Nested(field.schema.get_model(api, nested=True)))
        if "RelatedList" in str(type(field)):
            return restx_fields.List(restx_fields.Integer)

        return restx_fields.Integer

    def get_model(self, api, nested=False):
        my_fields = {field_name: self.transport_field_class(field, api, nested)
                     for field_name, field in self.fields.items()}
        return api.model(self.__class__.__name__, my_fields)


class UserSchema(SchemaDocSwagger):
    class Meta:
        # model class for the schema
        model = User
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    roles = fields.Nested(lambda: RoleSchema(exclude=("users", )), many=True)
    wines = fields.Nested(lambda: WineSchema(exclude=("users", )), many=True)


class RoleSchema( SchemaDocSwagger):
    class Meta:
        model = Role
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    users = fields.Nested(UserSchema(exclude=("roles", )), many=True)


class WineSchema( SchemaDocSwagger):
    class Meta:
        model = Wine
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    users = fields.Nested(UserSchema(exclude=("wines", )), many=True)


class Wine_typeSchema(SchemaDocSwagger):
    class Meta:
        model = Wine_type
        include_relationships = True
        load_instance = True
        sqla_session = db.session



class Wine_winerySchema(SchemaDocSwagger):
    class Meta:
        model = Wine_winery
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class PostSchema(SchemaDocSwagger):
    class Meta:
        model = Post
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class PointsSchema(SchemaDocSwagger):
    class Meta:
        model = Points
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    
    

