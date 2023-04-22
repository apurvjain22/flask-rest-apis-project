from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    """
    dump_only - Marshmallow will not check 'id' for validation when a data is coming from a request
    It will deal with below fields only, this schema wouldn't know about stores
    """

    id = fields.Int(dump_only=True)  # this is only required when we have to return data from an API to client
    name = fields.Str(required=True)  # this would be coming from the request hence it is a required parameter
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    """
    This schema will keep a note of below fields only, wouldn't know about the items
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemUpdateSchema(Schema):
    """
    only required below 2 fields for updating data in items
    """
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):
    """
    Now this fn will inherit PlainItemSchema + would add fields related to stores.
    fields.Nested means that it will add the fields corresponding to the PlainStoreSchema.
    ex:
        {
        "id": 1,
        "name": "item name",
        "price": 13.50,
        "store_id": 1,
        "store": {
            "id": 1,
            "name": "store name"
        }
    }
    """
    store_id = fields.Int(required=True, load_only=True)  # load_only be required when it would be used only for storing
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    """
    Similarly this fn is inheriting from PlainStoreSchema + will now have the info about the items fields as well
    fields.List, which means that we are expecting a list of items in contrast to ItemSchema where we expect a
    single store.
    ex:
        {
        "id": 1,
        "name": "store name",
        "items": [
            {"id": 1, "name": "item name", "price": 13.50},
            {"id": 2, "name": "item2 name", "price": 20.50}
        ]
    }
    """
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)

"""
After creating relationship in the models, nested relationships would be created among both the models
eg: in ItemsModel, there would be a Nested relationship among StoreModel object and in StoreModel with item model object 
So to reflect in the schemas, we have to change the modify the schemas according to models
1- We will be creating a separate schemas of both the models without relationship object
2- we will then create a new schema with their respective relationship object by inheriting the main schema
try and see the result 
3- 
"""
