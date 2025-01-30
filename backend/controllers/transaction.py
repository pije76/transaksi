from bson.objectid import ObjectId
from backend.connection import transaction_collection

from backend.controllers.user import *

def balance_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "user_id": data["user_id"],
        "balance": data["balance"],
    }

def transaction_helper(data) -> dict:
    return {
        # "id": str(data["_id"]),
        "id": str(data["_id"]),
        # "id": serializeDict(data["_id"]),
        # "user_id": data["user_id"],
        "user_id": str(data["user_id"]),
        "date_time": data["date_time"],
        "transaction_type": data["transaction_type"],
        "amount": data["amount"],
        "method": data["method"],
        "status": data["status"],
    }


# Retrieve all transaction present in the database
def retrieve_balance():
    balances = []
    for balance in balance_collection.find():
        # balance_id = str(balance["_id"])
        print(balance)
        print(type(balance))
        print(balance["balance"])
        # balances = balance_collection.find({'_id': ObjectId(balance_id)})
        # balances.append(balance_helper(balance))
        print(balances)
        print(type(balances))
    return balances

def retrieve_transactions():
    transactions = []
    for item in transaction_collection.find():
        # item = str(x["_id"])
        # response.append(id)
        # item = item["user_id"]
        # transaction_id = str(transaction["_id"])
        print("item", item)
        print(type(item))
        # print("transaction_collection", transaction_collection)
        # print(type(transaction_collection))
        # print(transaction["balance"])
        # transactions = transaction_collection.find({'_id': ObjectId(transaction_id)})
        transactions.append(transaction_helper(item))
        # transactions.append(item)
        # print(transactions)
        # print(type(transactions))
    return transactions


# Add a new transaction into to the database
def add_transaction(transaction_data: dict) -> dict:
    transaction = transaction_collection.insert_one(transaction_data)
    new_transaction = transaction_collection.find_one({"_id": transaction.inserted_id})
    return transaction_helper(new_transaction)


# Retrieve a transaction with a matching ID
def retrieve_transaction(id: str) -> dict:
    transaction = transaction_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        return transaction_helper(transaction)


# Update a transaction with a matching ID
def update_transaction(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    transaction = transaction_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        updated_transaction = transaction_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_transaction:
            return True
        return False


# Delete a transaction from the database
def delete_transaction(id: str):
    transaction = transaction_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        transaction_collection.delete_one({"_id": ObjectId(id)})
        return True
