from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException, Security, Body, status, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict

from bson.objectid import ObjectId
from datetime import datetime

from backend.auth import *
from backend.utils import *
from backend.connection import *
from backend.models.user import *
from backend.models.transaction import *


router = APIRouter()

default_balance = 0.0
current_dateTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

@router.post('/token')
def create_token(request: OAuth2PasswordRequestForm = Depends()):
    user = user_collection.find_one({"username": request.username})
    if not user:
        return ErrorResponseModel("An error occurred.", 404, "No user found with this username.")
    if not Hash.verify(user["password"], request.password):
        return ErrorResponseModel("An error occurred.", 404, "Incorrect password.")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post('/register')
def create_user(request: User):
    hashed_pass = Hash.bcrypt(request.password)
    username = request.username
    user_object = user_collection.find_one({"username": username})
    if user_object is not None:
        return ErrorResponseModel("An error occurred.", 400, "User with this username already exist.")
    else:
        user = user_collection.insert_one(
        {
            'username': username,
            'password': hashed_pass,
            'email': request.email,
            'payment_method': "",
            'payment_number': 0,
            'photo': "",
        })
        userid = user.inserted_id
        new_user = user_collection.find_one({"_id": userid})
        new_user = new_user["username"]
        balance = balance_collection.insert_one(
        {
            'user_id': userid,
            'balance': default_balance
        })
        balanceid = balance.inserted_id
        new_balance = balance_collection.find_one({"_id": balanceid})
        new_balance = new_balance["balance"]
        return ResponseModel(new_user, "User added successfully.")


@router.get("/", summary="Get All Users")
def get_users():
    users = []
    for item in user_collection.find():
        users.append(user_helper(item))
    if users:
        return ResponseModel(users, "User data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{id}", summary="Get User Detail")
def get_user_detail(id):
    user = user_collection.find_one({"_id": ObjectId(id)})
    user = user_helper(user)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.put("/{id}", summary="Update User Detail")
def update_user_data(
    id: str,
    username: constr(to_lower=True)=Form(None),
    password: str=Form(None),
    email: EmailStr=Form(None),
    payment_method: Literal['bank', 'emoney']=Form(None),
    payment_number: int=Form(None),
    # is_superuser: bool=Form(None),
    photo: UploadFile=File(None)
):

    user = UpdateUser(
        username=username,
        password=password,
        email=email,
        payment_method=payment_method,
        payment_number=payment_number,
        # is_superuser=is_superuser,
    )
    update_data = user.dict()
    try:
        if "password" in update_data:
            update_data["password"] = Hash.bcrypt(user.password)
    except:
        pass

    if photo is not None:
        fileName = update_data['username']
        folderName = 'profile'
        random_uid = str(uuid4())
        _, f_ext = os.path.splitext(photo.filename)
        picture_name = (random_uid if fileName==None else fileName.lower().replace(' ', '')) + f_ext
        path = os.path.join(upload_dir, folderName)

        if not os.path.exists(path):
            os.makedirs(path)

        picture_path = os.path.join(path, picture_name)
        update_data["photo"] = picture_path

        output_size = (200,200)
        img = Image.open(photo.file)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.thumbnail(output_size)
        img.save(picture_path, 'JPEG', quality=50)

    updated_user = user_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    if updated_user:
        return ResponseModel("Updated user with ID: {} is successful".format(id), "User updated successfully")
    return ErrorResponseModel("An error occurred", 404, "There was an error updating the user data.")


@router.delete("/{id}", summary="Delete User Data")
def delete_user_data(id: str):
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user_collection.delete_one({"_id": ObjectId(id)})
        return ResponseModel("User with ID: {} removed".format(id), "User deleted successfully")
    return ErrorResponseModel("An error occurred", 404, "User with id {0} doesn't exist".format(id))

