from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["transaksi"]
print("db", db)
posts = db.list_collection_names()



# all collections
user_collection = db['user']
balance_collection = db['balance']
# deposit_collection = db['deposit']
# withdraw_collection = db['withdraw']
transaction_collection = db['transaction']

# for item in posts:
#     for data in db[item].find({}):
#         print("data", data)
