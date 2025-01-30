

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
