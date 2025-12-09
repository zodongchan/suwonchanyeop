from fastapi import APIRouter, status, Depends
from datetime import datetime
from schemas import DiaryCreate, DiaryUpdate, DiaryResponse
from auth import AuthenticatedUser
from typing import List

router = APIRouter(prefix="/diaries", tags=["Diary"])

fake_db = {
    1: {"id": 1, "user_id": 100, "title": "첫 일기", "content": "오늘 하루는 좋았다.", "created_at": datetime.now(), "updated_at": datetime.now()},
    2: {"id": 2, "user_id": 200, "title": "남의 일기", "content": "이건 다른 사용자의 글이다.", "created_at": datetime.now(), "updated_at": datetime.now()},
}

@router.get("/", response_model=List[DiaryResponse])
def read_diaries(current_user_id: AuthenticatedUser):
    user_diaries = [
        entry 
        for entry in fake_db.values() 
        if entry["user_id"] == current_user_id
    ]
    
    return user_diaries

@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
def create_diary(
    diary_data: DiaryCreate, 
    current_user_id: AuthenticatedUser
):
    new_id = max(fake_db.keys()) + 1 if fake_db else 1
    
    new_entry = {
        "id": new_id,
        "user_id": current_user_id,
        "title": diary_data.title,
        "content": diary_data.content,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    fake_db[new_id] = new_entry
    return new_entry


@router.get("/{diary_id}", response_model=DiaryResponse)
def read_diary(
    diary_id: int, 
    current_user_id: AuthenticatedUser 
):
    diary_entry = fake_db.get(diary_id)
    if not diary_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diary not found")
    return diary_entry


@router.patch("/{diary_id}", response_model=DiaryResponse)
def update_diary(
    diary_id: int,
    update_data: DiaryUpdate,
    current_user_id: AuthenticatedUser
):
    diary_entry = fake_db.get(diary_id)
    if not diary_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diary not found")
    if diary_entry["user_id"] != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this diary")
    if update_data.title is not None:
        diary_entry["title"] = update_data.title
    if update_data.content is not None:
        diary_entry["content"] = update_data.content
    diary_entry["updated_at"] = datetime.now()

    return diary_entry


@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_diary(
    diary_id: int, 
    current_user_id: AuthenticatedUser
):
    diary_entry = fake_db.get(diary_id)
    if not diary_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diary not found")
    if diary_entry["user_id"] != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this diary")
    del fake_db[diary_id]
    return