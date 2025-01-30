from fastapi import APIRouter, Body, FastAPI, HTTPException, Query, Depends, status, Response, Request, Security
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, ValidationError
from typing import List
from bson import ObjectId

from backend.auth import *
from backend.utils import *
from backend.connection import *
from backend.controllers.transaction import *
from backend.models.transaction import *

router = APIRouter()

current_dateTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

@router.get("/balance", summary="Get Balance Data from Logged-in User")
def get_balance(current_user: User=Depends(get_current_user)):
    user_id = current_user['_id']
    transaction = balance_collection.find_one({"user_id": user_id})
    balance = transaction['balance']
    if balance:
        return ResponseModel(balance, "Balance data retrieved successfully")
    return ResponseModel(balance, "Empty list returned")




@router.get("/history", summary="GET All History Data from Logged-in User")
def get_transaction(request: Request, current_user: User=Depends(get_current_user)):
    user_id = current_user['_id']
    transactions = []
    transaction1 = request.url.query
    transaction = transaction_collection.find(
    {
        "user_id": user_id
    })

    for item in transaction:
        item["_id"] = str(item["_id"])
        item["user_id"] = str(item["user_id"])
        item["date_time"] = str(item["date_time"])
        transactions.append(item)
    if transactions:
        return ResponseModel(transactions, "History data retrieved successfully")
    return ResponseModel(transactions, "Empty list returned")


@router.get("/{id}", summary="Get History Detail")
def get_transaction_detail(id):
    transaction = transaction_collection.find_one({"_id": ObjectId(id)})
    result = serializeDict(transaction)
    result = transaction_helper(transaction)
    if result:
        return ResponseModel(result, "History Detail retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "History doesn't exist.")


@router.put("/{id}", summary="Update User Detail")
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
    update_data = transaction.dict()
    updated_transaction = transaction_collection.update_one({"_id": ObjectId(request.transaction_id)}, {"$set": update_data})

    if updated_transaction:
        return ResponseModel("Updated transaction with ID: {} is successful".format(ObjectId(request.transaction_id)), "User updated successfully")
    return ErrorResponseModel("An error occurred", 404, "There was an error updating the transaction data.")


@router.delete("/history/{id}", summary="Delete History Data")
def delete_user_data(id: str):
    transaction = transaction_collection.find_one({"_id": ObjectId(id)})
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

