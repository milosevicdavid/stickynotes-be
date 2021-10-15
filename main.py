from fastapi import FastAPI
from pydantic import BaseModel
from mongoengine import connect
from models import ItemModel
import json
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware


connect(db="itemmodel", host="localhost", port=27017)

app = FastAPI()

origins = [
        "*"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    title: str
    content: str
    color: str

@app.get("/")
async def get_all():
    allitems = []
    for item in ItemModel.objects:
        id_conv = str(ObjectId(item.id))
        converteditem =  { 'id': id_conv, 'title': item.title, 'content': item.content, 'color': item.color}    
        allitems.append(converteditem)
    return allitems

@app.post("/")
async def post_item(item: Item):
    newitem = ItemModel(title=item.title, content=item.content, color=item.color )
    newitem.save()
    return json.loads(newitem.to_json())

@app.get("/{item_id}")
async def get_item(item_id: str):
    oneitem = ItemModel.objects.get(id=ObjectId(item_id))
    print(ObjectId(item_id))
    return json.loads(oneitem.to_json())

@app.put("/{item_id}")
async def change_item(item_id, item: Item):
    ItemModel.objects(id=ObjectId(item_id)).update(title=item.title, content=item.content, color=item.color)
    oneitem = ItemModel.objects.get(id=ObjectId(item_id))
    return json.loads(oneitem.to_json())


@app.delete("/{item_id}")
async def delete_item(item_id: str):
    ItemModel.objects(id=ObjectId(item_id)).delete()
    return "Item deleted"

