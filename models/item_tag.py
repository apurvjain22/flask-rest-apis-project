from db import db


class ItemTag(db.Model):
    __tablename__ = "item_tag"

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
