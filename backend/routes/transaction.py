from fastapi import APIRouter, Body, FastAPI, HTTPException, Query, Depends, status, Response, Request, Security
from fastapi.encoders import jsonable_encoder

# from pymongo.synchronous import cursor

# from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel, ValidationError
from typing import List
from bson import ObjectId

from backend.auth import *
from backend.connection import *
from backend.controllers.transaction import *
from backend.models.transaction import *

router = APIRouter()

# current_dateTime = datetime.now()
current_dateTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

@router.get("/balance", summary="Get Balance Data from Logged-in User")
def get_balance(current_user: User=Depends(get_current_user)):
    # username = current_user['username']
    user_id = current_user['_id']
    print("user_id", user_id)
    transaction = balance_collection.find_one({"user_id": user_id})
    print("transaction", transaction)
    balance = transaction['balance']
    print("balance", balance)
    if balance:
        return ResponseModel(balance, "Balance data retrieved successfully")
    return ResponseModel(balance, "Empty list returned")


#APIs for Transbackend.action logs
# @router.get("/history", status_code=status.HTTP_200_OK, summary="Get history of transactions")
# def get_balance_history(
#     params: CreateBalance = Depends(),
#     credentials: HTTPAuthorizationCredentials = Security(security),
#     authorize: AuthJWT = Depends(),
# ):
#     authorize.jwt_required()
#     email = authorize.get_jwt_subject()
#     user = user_controller.get_or_404(email=email, session=session)
#     user_balance = balance_controller.get_or_404(user_id=user.guid, currency=params.currency, session=session)
#     return (
#         [ShowTransaction.from_orm(transaction) for transaction in user_balance.transactions]
#         if user_balance.transactions
#         else None
#     )


@router.get("/history", summary="GET All History Data from Logged-in User")
def get_transaction(request: Request, current_user: User=Depends(get_current_user)):
    user_id = current_user['_id']
    print("user_id", user_id)
    transactions = []
    # transaction1 = request.query_params['transaction_type']
    # transaction1 = request.query_params
    transaction1 = request.url.query
    print("transaction1", transaction1)
    transaction = transaction_collection.find(
    {
        "user_id": user_id
    })
    # transaction = transaction_collection.find(
    # {
    #     rated:
    #     {
    #         $in:
    #         [
    #             "PG",
    #             "PG-13"
    #         ]
    #     }
    # })
    # transaction = transaction_collection.find(
    # {
    #     "user_id": user_id,
    #     "transaction_type":
    #     {
    #         transaction_type
    #     }
    # })
    # transaction = transaction_collection.find({ObjectId: user_id})
    # transaction = transaction['date_time']
    # transaction = transaction(transaction_collection, {"user_id": user_id})
    print("transaction", transaction)
    for item in transaction:
        item["_id"] = str(item["_id"])
        item["user_id"] = str(item["user_id"])
        # item["date_time"] = str(date)[:19]
        item["date_time"] = str(item["date_time"])
        print("item", item)
        print(type(item))
        transactions.append(item)
        # item["_id"] = {"$toString": "$_id"}
        print("transactions", transactions)
    if transactions:
        # return ResponseModel(transactions, "History data retrieved successfully")
        return ResponseModel(transactions, "History data retrieved successfully")
    # if transactions is None:
    #     # return ResponseModetransactionl(transactions, "History data retrieved successfully")
    #     return ResponseModel(transactions, "Empty list returned")
    # return ErrorResponseModel("An error occurred", 404, "There was an error updating the history data.")
    return ResponseModel(transactions, "Empty list returned")


@router.get("/{id}", summary="Get History Detail")
def get_transaction_detail(id):
    transaction = transaction_collection.find_one({"_id": ObjectId(id)})
    result = serializeDict(transaction)
    result = transaction_helper(transaction)
    if result:
        return ResponseModel(result, "History Detail retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "History doesn't exist.")


# @router.put("/history/{id}", summary="Update History Detail")
# def update_transaction_data(id: str, request:TransactionUpdate):
#     request = {k: v for k, v in request.dict().items() if v is not None}
#     # transaction_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"photo":photo}})
#     updated_transaction = update_transaction(id, request)
#     if updated_transaction:
#         return ResponseModel("History data updated successfully")
#     return ErrorResponseModel("An error occurred", 404, "There was an error updating the history data.")


@router.put("/{id}", summary="Update User Detail")
# def update_transaction_data(
#     id: str,
#     username: constr(to_lower=True)=Form(None),
#     password: str=Form(None),
#     email: EmailStr=Form(None),
#     payment_method: Literal['bank', 'emoney']=Form(None),
#     payment_number: int=Form(None),
#     # is_superuser: bool=Form(None),
#     photo: UploadFile=File(None)
# ):
def update_transaction_data(request: Annotated[TransactionUpdate, Form()]):
    transaction = TransactionUpdate(
        transaction_id=request.transaction_id,
        user_id=request.user_id,
        date_time=request.date_time,
        transaction_type=request.transaction_type,
        amount=request.amount,
        method=request.method,
        status=request.status,
    )
    print("request", request)
    update_data = transaction.dict()
    # try:
    #     if "password" in update_data:
    #         update_data["password"] = Hash.bcrypt(transaction.password)
    # except:
    #     pass
    print("update_data", update_data)
    print(type(update_data))
    # transaction = request.dict()
    # transaction["transaction_id"] = transaction.pop("_id")

    # print("transaction", transaction)
    # print(type(transaction))
    # user = transaction_collection.find_one({"username": request.username})

    # updated_transaction = transaction_collection.update_one({"_id": request.transaction_id}, {"$set": update_data})
    updated_transaction = transaction_collection.update_one({"_id": ObjectId(request.transaction_id)}, {"$set": update_data})

    if updated_transaction:
        return ResponseModel("Updated transaction with ID: {} is successful".format(ObjectId(request.transaction_id)), "User updated successfully")
    return ErrorResponseModel("An error occurred", 404, "There was an error updating the transaction data.")

# @router.post("/history", summary="POST history data")
# # def add_transaction_data(transaction: TransactionCreate):
# def add_transaction_data(transaction: TransactionCreate, transaction_type: Choices):
#     transaction = jsonable_encoder(transaction)
#     transaction = transaction_collection.insert_one(transaction)
#     choices = transaction_type.value
#     # user = jsonable_encoder(user)
#     # new_user = add_user(user)
#     # new_transaction = transaction_collection.find_one({"_id": transaction.inserted_id})
#     # transaction = jsonable_encoder(transaction).dict()
#     # new_transaction = add_transaction(transaction)
#     new_transaction = transaction_collection.insert_one(transaction)
#     # new_transaction = transaction_collection.insert_one(transaction.model_dump(by_alias=True, exclude=["id"]))
#     return ResponseModel(new_transaction, "Transaction added successfully.")

@router.delete("/history/{id}", summary="Delete History Data")
def delete_user_data(id: str):
    transaction = transaction_collection.find_one({"_id": ObjectId(id)})
    # user: Annotated[User, Depends(Authorization(allowed_roles=[UserRole(name='admin')]))]
    if transaction:
        transaction_collection.delete_one({"_id": ObjectId(id)})
        return ResponseModel("Transaction with ID: {} removed".format(id), "Transaction deleted successfully")
    return ErrorResponseModel("An error occurred", 404, "Transaction with id {0} doesn't exist".format(id))


# Adding a New Deposit
@router.post("/deposit", summary="Post Deposit for Logged-in User")
def add_deposit(request: DepositBase, current_user: User=Depends(get_current_user)):
    user_id = current_user['_id']
    users = []
    transaction = balance_collection.find_one({"user_id": user_id})
    balance = transaction['balance']
    request: DepositBase
    item_dict = request.dict()
    deposit = item_dict['amount']
    total_balance = balance + deposit
    balance_collection.update_one({'user_id': user_id}, {"$set": {"balance": total_balance}})
    # transaction_collection.update_one({'user_id': user_id}, {
    #     "$set": {
    #         "user_id": user_id,
    #         "transaction_type": transaction_type,
    #     }
    # })
    transaction = transaction_collection.insert_one(
    {
        "user_id": user_id,
        "date_time": current_dateTime,
        "transaction_type": "deposit",
        "amount": deposit,
        "method": "bank",
        "status": "pending"
    })
    transactionid = transaction.inserted_id
    new_transaction = transaction_collection.find_one({"_id": transactionid})
    new_transaction = new_transaction["transaction_type"]
    return ResponseModel(deposit, "Deposit successfully.")


@router.post("/withdraw", summary="Post Withdraw for Logged-in User")
def add_withdraw(request: WithdrawBase, current_user: User=Depends(get_current_user)):
    username = current_user['username']
    user_id = current_user['_id']
    transaction = balance_collection.find_one({"user_id": user_id})
    balance = transaction['balance']
    request: DepositBase
    item_dict = request.dict()
    withdraw = item_dict['amount']
    total_balance = balance - withdraw
    if total_balance < 0:
        return ErrorResponseModel("An error occurred.", 400, "Can not withdraw! Insufficient balance.")
    balance_collection.update_one({'user_id': user_id}, {"$set": {"balance": total_balance}})
    transaction = transaction_collection.insert_one(
    {
        "user_id": user_id,
        "date_time": current_dateTime,
        "transaction_type": "withdraw",
        "amount": withdraw,
        "method": "bank",
        "status": "pending"
    })
    transactionid = transaction.inserted_id
    new_transaction = transaction_collection.find_one({"_id": transactionid})
    new_transaction = new_transaction["transaction_type"]
    return ResponseModel(withdraw, "Withdraw successfully.")

