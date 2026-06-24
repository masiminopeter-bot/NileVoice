from fastapi import APIRouter

router = APIRouter()

@router.get("/submissions")
def submissions_root():
    return {"message": "submissions"}
