from db import db


class StoreModel(db.Model):
    """
    We are defining StoreModel as per one-to-many relationship i.e. one store can have multiple items.
    items:  We don't have item_id in the StoreModel but with db.relationship() that items variable back populates to
            store and in ItemModel, store variable back populates to items variable. So by this sqlalchemy knows the
            relationship b/w 2 models.
            This would populate all the items, with respective store id
            back_populates: Sqlalchemy knows these two fields are related now, and will update each as the other is
                            updated.
            lazy:   It determines how the related objects get loaded when querying through relationships.
                    Typically, when we query from the db, the data get loaded at once, and it allows us the alternate
                    way they get loaded.
                    dynamic:    here items data won't get populated when we query the db until and unless we
                                explicitly call it
            cascade:    It will delete the FK relationship i.e. will delete items associated with particular store_id
    > Like in StoreModel we have store_id column, we don't have it here because through back_populates field present in
    both the models, we know that these are 2 ends of the relationship.
    > w.r.t schema, stores model will have nested item objects
    """
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(88), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic", cascade="all, delete")
