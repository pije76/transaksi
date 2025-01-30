from pydantic import BaseModel, ConfigDict
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, Union
from typing_extensions import Annotated
from bson.decimal128 import Decimal128
from bson.objectid import ObjectId as BsonObjectId

from datetime import datetime
from decimal import Decimal
from enum import Enum

from backend.models.user import *
from backend.auth import *


class Choices(str, Enum):
	deposit = "deposit"
	withdraw = "withdraw"

# class Method(Enum):
class Method(str, Enum):
	cash = 'cash'
	bank = 'bank'
	emoney = 'emoney'


class BalanceBase(BaseModel):
	balance_id: str = Field(..., alias='_id')
	user_id : User
	# balance: float = None
	balance: float = 0.0

	model_config = ConfigDict(
		populate_by_name=True,
		arbitrary_types_allowed=True,
	)


# class BalanceCreate(BalanceBase):
# 	# currency: str = "USD"
# 	# amount: Optional[str] = "0"
# 	pass


class DepositBase(BaseModel):
	# deposit_id: str = Field(..., alias='_id')
	amount: float
	method: Literal['bank', 'emoney']
	# status: Literal['pending', 'success', 'failed']

	model_config = ConfigDict(
		populate_by_name=True,
		arbitrary_types_allowed=True,
	)

class DepositCreate(DepositBase):
	pass


class WithdrawBase(BaseModel):
	# withdraw_id: str = Field(..., alias='_id')
	amount: float
	method: Literal['bank', 'emoney']
	# status: Literal['pending', 'success', 'failed']

	model_config = ConfigDict(
		populate_by_name=True,
		arbitrary_types_allowed=True,
	)

class WithdrawCreate(WithdrawBase):
	pass


class TransactionBase(BaseModel):
	transaction_id: str = Field(..., alias='_id')
	# user_id : User
	user_id: str
	# date_time: datetime
	date_time: Optional[datetime] = None
	# transaction_type: Literal['deposit', 'withdraw']
	# amount: float
	# method: Literal['bank', 'emoney']
	# status: Literal['pending', 'success', 'failed']


	model_config = ConfigDict(
		populate_by_name=True,
		arbitrary_types_allowed=True,
	)

class TransactionCreate(TransactionBase):
	pass

class TransactionUpdate(TransactionBase):
	transaction_type: Literal['deposit', 'withdraw']
	amount: float
	method: Literal['bank', 'emoney']
	status: Literal['pending', 'success', 'failed']



def ResponseModel(data, message):
	return {
		"data": [data],
		"code": 200,
		"message": message,
	}

def ErrorResponseModel(error, code, message):
	return {"error": error, "code": code, "message": message}
