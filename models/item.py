from db import db


class ItemModel(db.Model):  # using db.Model, will define relationship b/w row of a table with python class i.e. object
    """
    We are defining the ItemModel as per many-to-one relationship i.e. multiple items will have one store only
    store_id: It would fetch id from store table after matching store id with item id i.e. having a foreign key relationship
    store: After having store_id coming as a foreign key, this would populate the object of StoreModel whose store_id
           in ItemModel matches with id column in ItemModel
           > w.r.t schema, item model will have nested list of store model object
    """
    __tablename__ = "items"  # table name

    id = db.Column(db.Integer, primary_key=True)  # would be prepopulated and would be auto incrementing
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="item_tag")
