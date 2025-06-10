from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.posts.db import add_to_db, delete_to_db, update_to_db
from app.posts.models import PostModel
from app.posts.schemas import Post, PostAdd, PostDelete, PostUpdate
from app.posts.utils import (get_check_new_title, get_check_post,
                             get_check_post_in_db)
from app.users.auth import get_db
from app.users.models import UserModel
from app.users.user import get_current_user

router = APIRouter(tags=["Посты"])


@router.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    return db.query(PostModel).all()


@router.post("/post/add")
def add_to_post(data_post: PostAdd, db: Session = Depends(get_db)):
    try:
        get_check_post(data_post.title, db=db)
        add_to_db(
            data_post.title,
            data_post.content,
            db=db,
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return {
        "Добавлен пост": {
            "title": data_post.title,
            "content": data_post.content,
        }
    }


@router.patch("/post/update")
def update_post(
    data_post: PostUpdate,
    user_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        get_check_post_in_db(title=data_post.title, db=db)
        get_check_new_title(new_title=data_post.new_title, db=db)
        update_to_db(
            title=data_post.title,
            new_title=data_post.new_title,
            new_content=data_post.content,
            db=db,
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return {"Изменен пост": data_post.title}


@router.delete("/post/delete")
def delete_to_post(data_post: PostDelete, db: Session = Depends(get_db)):
    try:
        get_check_post_in_db(title=data_post.title, db=db)
        delete_to_db(title=data_post.title, db=db)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return {"Удален пост": data_post.title}
