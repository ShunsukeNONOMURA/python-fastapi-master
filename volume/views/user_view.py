import json
from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum, unique

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, RootModel, SecretStr

from db import TUser, VUser, create_session

router = APIRouter()

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
    def __eq__(self, other: DDDModel)->bool:
        if other is None or type(self) != type(other):
            return False # isinstance(other, Entity)を除去
        return self._id() == other._id()
    def __ne__(self, other: DDDModel)->bool:
        return not self.__eq__(other)

@unique
class UserRoleEnum(Enum):
    Admin = "00"
    General = "10"
    Guest = "99"

class User(Entity):
    class UserId(ValueObject, RootModel):
        root: str
    class UserPassword(ValueObject, RootModel):
        root: SecretStr
    class UserName(ValueObject, RootModel):
        root: str
    class UserRoleCode(ValueObject, RootModel):
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
    user_role_code: UserRoleCode
    user_role_name: UserRoleName
    user_creation_datetime: UserCreationDatetime
    user_update_datetime: UserUpdateDatetime

    def _id(self):
        return self.user_id

    model_config = ConfigDict(from_attributes=True)


class UserRepository:
    def find(self, user_id: str):
        with create_session() as session:
            orm = session.query(VUser).filter(VUser.user_id == user_id).first()
            # orm = session.query(TUser).filter(TUser.user_id == user_id).first()
            return User.model_validate(orm) if orm is not None else None
    def query(self):
        with create_session() as session:
            users = session.query(VUser).all()
            # return users
            return [User.model_validate(orm) for orm in users]
    def insert(self, user: User):
        with create_session() as session:
            orm = session.query(TUser).filter(TUser.user_id == user.user_id.root).first()
            user = TUser(
                user_id = "guest",
                user_name = "guest",
                user_password = "guest",
                user_role_code = "99",
            )
            session.add(orm)
            session.commit()
    def delete(self, user: User):
        with create_session() as session:
            orm = session.query(TUser).filter(TUser.user_id == user.user_id.root).first()
            session.delete(orm)
            session.commit()

@router.get("/users/{user_id}", tags=["user"])
def get_user(user_id: str):
    user_repository = UserRepository()
    user = user_repository.find(user_id)
    return user

@router.get("/query/users", tags=["user"])
def query_user(q: str = ""):
    user_repository = UserRepository()
    users = user_repository.query()
    return users
    return {"q": q}

@router.post("/users", tags=["user"])
def create_user(user: User):
    # user = User.model_validate(
    #     user
    # )
    user_repository = UserRepository()
    user = user_repository.insert(user)
    return user

@router.delete("/users/{user_id}", tags=["user"])
def delete_user(user_id: str):
    user_repository = UserRepository()
    user = user_repository.find(user_id)
    user = user_repository.delete(user)
    return user
