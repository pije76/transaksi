
def transaction_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "user_id": str(data["user_id"]),
        "date_time": data["date_time"],
        "transaction_type": data["transaction_type"],
        "amount": data["amount"],
        "method": data["method"],
        "status": data["status"],
    }

