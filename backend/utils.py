
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

def serializeDict(entity) -> dict:
    if entity!=None:
        return {**{i:str(entity[i]) for i in entity if i=='_id'}, **{i:entity[i] for i in entity if i!='_id'}}
    return None


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
