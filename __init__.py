""" Whenever models would be imported in any module, this file would get executed first and
    we can directly use models import ItemModel or StoreModel """

from models.store import StoreModel
from models.item import ItemModel
from models.tag import TagModel
from models.item_tag import ItemTag
from models.user import UserModel
