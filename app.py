import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    """
    This fn will create, setup and configure the flask app
    :param db_url: if given we will connect to the provided db
    :return: flask app
    """
    # creating an instance of a flask class by passing application's module or package name, and
    # we are also passing data.db path as now data.db is created under instance folder
    app = Flask(__name__, instance_path=os.getcwd())
    # configuration options
    app.config[
        "PROPAGATE_EXCEPTIONS"] = True  # if any exceptions occurs in the extension of flask, propagate it into the main app so that we can see it
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"  # standard for api documentation
    app.config["OPENAPI_URL_PREFIX"] = "/"  # it tells where the root of the api is
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # defining database url
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # making connection b/w sqlalchemy and flask app
    migrate = Migrate(app, db)

    api = Api(app)  # connects flask-smorest extension to the flask app

    app.config['JWT_SECRET_KEY'] = "apurv"  # this is used for signing the JWT token
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        """ Every time we receive a token this fn would check if the token is present in the blocklist or not
            If present in the blocklist that means that the user has already logged out and that token is no longer
            in use
            jti - JWT unique Identifier"""
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """ This fn would return the error msg to the client when the token is present in the blocklist"""
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ), 401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}, 401, )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid token"}, 401, )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"description": "Request does not contain access token",
                        "error": "authorized_required"
                        }, 401, )

    # this will create db with tables(that are in models) when making a first request
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
