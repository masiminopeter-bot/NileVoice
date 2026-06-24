from fastapi import APIRouter

router = APIRouter()

@router.get("/languages")
def language_root():
    return {"message": "languages"}
