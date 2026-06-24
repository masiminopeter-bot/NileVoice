from fastapi import APIRouter

router = APIRouter()

@router.get("/translate")
def translate_root():
    return {"message": "translate"}
