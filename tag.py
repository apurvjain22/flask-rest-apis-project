from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from db import db
from schemas import TagSchema, TagAndItemSchema, PlainTagSchema
from models import TagModel, StoreModel, ItemModel

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """ It will give list of tags and items associated with a store """
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    @jwt_required()
    def post(self, tag_data, store_id):
        """ new tag is created by attaching to existing store """
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    @jwt_required()
    def post(self, item_id, tag_id):
        """ link items to tags """
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag")

        return tag

    @blp.response(200, TagAndItemSchema)
    @jwt_required()
    def delete(self, item_id, tag_id):
        """ fn to unlink items from tag"""
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting a tag")

        return {'message': "Item removed from tag", "item": item, "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202, description="Deletes a tag if no item is tagged with it", example={'message': "Tag deleted"})
    @blp.alt_response(404, description="Tag not found")
    @jwt_required()
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        try:
            if not tag.items:
                db.session.delete(tag)
                db.session.commit()
                return {'message': "Tag deleted"}
        except SQLAlchemyError:
            abort(400,
                  message="Could not delete tag. Make sure tag is not associated with any items, then try again")


@blp.route("/tag")
class Tags(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()
