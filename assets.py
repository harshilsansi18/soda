from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_assets():
    return {"message": "List of assets"}
