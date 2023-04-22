import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema, PlainStoreSchema
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

## Blueprint
# It registers info in an API documentation
# 1st: name "stores" and this name will be used in the future if we ever gonna used to create links b/w 2 blueprint
# 2nd: unique name, so we just we pass __name__
# 3rd: description
blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")  # blp connecting flask-smorest to Flask MethodView
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """ fetching specific store id from the db"""
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id):
        """ We are not decorating the response in delete method because delete is just returning the message
        not any data. So it is not necessary to decorate those"""
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))  # many=True - as many stores would be present, so to show multiple
    # stores through an /store endpoint we are mentioning many=True
    def get(self):
        return StoreModel.query.all()

    # @blp.arguments is a validator. So whenever user sends the json, this argument/validator will check all the fields
    # are present and its type  and then sends back the json in the form of parameter i.e. store_data in here
    # in the swagger it will also tell what should be the response json
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    @jwt_required()
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")
        return store, 201
