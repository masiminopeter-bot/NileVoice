from fastapi import APIRouter

router = APIRouter()

@router.get("/dictionary")
def dictionary_root():
    return {"message": "dictionary"}
