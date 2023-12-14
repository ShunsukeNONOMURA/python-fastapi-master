from fastapi import APIRouter, HTTPException
router = APIRouter()

from pydantic import validator, SecretStr, BaseModel, RootModel, Field, ConfigDict
from datetime import datetime, timedelta, date
from typing import List, Optional, Any, Union
from enum import Enum, IntEnum, unique
from abc import ABCMeta, abstractmethod
import json

class DDDModel(BaseModel, metaclass=ABCMeta):
    def to_json(self):
        return json.loads(self.json())

class ValueObject(DDDModel, metaclass=ABCMeta):
    # class Config:
    #     allow_mutation = False
    model_config = ConfigDict(frozen=True)

class Entity(DDDModel, metaclass=ABCMeta):
    @abstractmethod
    def _id(self): # IDの取得方法を必ず設計する
        raise NotImplementedError

    # IDで比較するロジック
    def __eq__(self, other):
        if other is None or type(self) != type(other): return False # isinstance(other, Entity)を除去
        return self._id() == other._id()
    def __ne__(self, other):
        return not self.__eq__(other)

@unique
class UserRoleEnum(Enum):
    Admin = '00'
    General = '10'
    Guest = '99'

class User(Entity):
    class UserId(ValueObject, RootModel):
        root: str
    class UserPassword(ValueObject, RootModel):
        root: SecretStr
    class UserName(ValueObject, RootModel):
        root: str
    class UserRoleCd(ValueObject, RootModel):
        root : UserRoleEnum = Field(description="ユーザロール")
    class UserRoleName(ValueObject, RootModel):
        root : str
    class UserCreationDatetime(ValueObject, RootModel):
        root: datetime
    class UserUpdateDatetime(ValueObject, RootModel):
        root: datetime
    
    user_id: UserId
    user_password: UserPassword
    user_name: UserName
    user_role_cd: UserRoleCd
    user_role_name: UserRoleName
    user_creation_datetime: UserCreationDatetime
    user_update_datetime: UserUpdateDatetime

    def _id(self):
        return self.user_id
    
    model_config = ConfigDict(from_attributes=True)

from db import TUser, VUser, create_session
class UserRepository():
    def find(self, user_id: str):
        with create_session() as session:
            orm = session.query(VUser).filter(VUser.user_id == user_id).first()
            # orm = session.query(TUser).filter(TUser.user_id == user_id).first()
            print(orm)
            return User.model_validate(orm) if orm is not None else None
        
@router.get("/user/{user_id}", tags=["user"])
def get_user(user_id: str):
    user_repository = UserRepository()
    user = user_repository.find(user_id)
    return user

@router.get("/query/user", tags=["user"])
def query_user(q: str = None):
    return {"q": q}