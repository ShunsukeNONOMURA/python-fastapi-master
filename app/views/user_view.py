from fastapi import APIRouter, HTTPException
router = APIRouter()

@router.get("/user/{user_id}", tags=["user"])
def get_user(user_id: str):
    return {"user_id": user_id}

@router.get("/query/user", tags=["user"])
def query_user(q: str = None):
    return {"q": q}