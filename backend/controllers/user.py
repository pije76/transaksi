from bson.objectid import ObjectId
from PIL import Image
from uuid import uuid4

import os

from backend.connection import user_collection
from backend.auth import *
from backend.models.user import *
from backend.models.transaction import *

upload_dir = 'frontend/uploads'

# ================================================== #
def user_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "username": data["username"],
        "email": data["email"],
        "payment_number": data["payment_number"],
        "payment_method": data["payment_method"],
        "photo": data["photo"],
    }

# ================================================== #
def retrieve_users():
    users = []
    for item in user_collection.find():
        # print("item", item)
        # print(type(item))
        users.append(user_helper(item))
    return users

def retrieve_user(id: str) -> dict:
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

def add_user(user_data: dict) -> dict:
    # hashed_password = hash_password(user.password)
    # new_user = models.User(email=user.email, password=hashed_password)
    user = user_collection.insert_one(user_data)
    # balance = transaction_collection.insert_one(balance_data)
    # user = user.createIndex( { user_data.email: 1 }, { unique: true } )
    new_user = user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Update a user with a matching ID
def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False

# Delete a user from the database
def delete_user(id: str):
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user_collection.delete_one({"_id": ObjectId(id)})
        return True

# ================================================== #

def serializeDict(entity) -> dict:
    if entity!=None:
        return {**{i:str(entity[i]) for i in entity if i=='_id'}, **{i:entity[i] for i in entity if i!='_id'}}
    return None


def serializeList(entities) -> list:
    return [serializeDict(entity) for entity in entities]

def getById(id):
    return serializeDict(user_collection.find_one({"_id": ObjectId(id)}))

def resultVerification(id: ObjectId) -> dict:
    result = getById(id)
    ErrorResponseModel(result, 404, "There was an error updating the user data.")
    return result

def save_picture(file, folderName:str='', fileName:str=None):
    random_uid = str(uuid4())
    _, f_ext = os.path.splitext(file.filename)

    picture_name = (random_uid if fileName==None else fileName.lower().replace(' ', '')) + f_ext
    path = os.path.join(upload_dir, folderName)

    if not os.path.exists(path):
        os.makedirs(path)

    picture_path = os.path.join(path, picture_name)

    output_size = (125,125)
    img = Image.open(file.file)

    img.thumbnail(output_size)
    img.save(picture_path)

    return f'{upload_dir}/{folderName}/{picture_name}'

def savePicture(id, photo:str) -> bool:
    user_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"photo":photo}})
    return True
