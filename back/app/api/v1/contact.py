from fastapi import APIRouter

router = APIRouter()

@router.get("/contacts")
def contacts_root():
    return {"message": "contacts"}
