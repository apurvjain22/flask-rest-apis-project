from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

## Blueprint
# 1st: name "items" and this name will be used in the future if we ever gonna used to create links b/w 2 blueprint
# 2nd: unique name, so we just we pass __name__
# 3rd: description
blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)  # for API documentation
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    @jwt_required()
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        # item = ItemModel.query.get_or_404(item_id)
        if item:  # if item exist, data will be updated
            item.price = item_data['price']
            item.name = item_data['name']
        else:  # if the item doesn't exist then it will create
            item = ItemModel(id=item_id, **item_data)  # as creating a new resource so assigning same item_id to id

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    @jwt_required()
    def post(self, item_data):
        """
        create new item
        :param item_data: The requested json payload is being validated by marshmallow i.e. by ItemSchema
        and then those validated data is passed to an argument(item_data) as a dictionary.
        So we no longer required to use request.json() to accept the json payload.
        :return:
        """

        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")
        return item, 201
