from app.posts.models import PostModel


def add_to_db(title, content, db):
    data = PostModel(
        title=title,
        content=content
    )
    db.add(data)
    db.commit()
    db.refresh(data)


def update_to_db(title, new_title, new_content, db):
    data = db.query(PostModel).filter(PostModel.title == title).first()
    if not new_title:
        new_title = data.title
    if not new_content:
        new_content = data.content
    data.title = new_title
    data.content = new_content
    db.commit()
    db.refresh(data)


def delete_to_db(title, db):
    data = db.query(PostModel).filter(PostModel.title == title).first()
    db.delete(data)
    db.commit()
