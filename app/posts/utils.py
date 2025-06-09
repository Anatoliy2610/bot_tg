from app.posts.models import PostModel


def get_check_post(title, db):
    data = db.query(PostModel).filter(PostModel.title == title).first()
    if data:
        raise ValueError("Пост уже существует")


def get_check_post_in_db(title, db):
    data = db.query(PostModel).filter(PostModel.title == title).first()
    if not data:
        raise ValueError("Пост не найден")

def get_check_new_title(new_title, db):
    data = db.query(PostModel).filter(PostModel.title == new_title).first()
    if data:
        raise ValueError("Такое название поста уже существует")

