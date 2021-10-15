from mongoengine import Document, StringField, IntField

class ItemModel(Document):
    title = StringField(max_length=100)
    content = StringField(max_length=10000)
    color = StringField(max_length=100)

