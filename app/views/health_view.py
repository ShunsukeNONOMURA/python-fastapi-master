from fastapi import APIRouter, HTTPException
router = APIRouter()

@router.get("/health", tags=["health"])
def get_health():
    return {"msg": "ok"}