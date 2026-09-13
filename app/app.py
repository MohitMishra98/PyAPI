from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from app.schemas import PostCreate, PostCreateResponse, UserRead, UserUpdate, UserCreate

from app.db import Post, create_db_and_tables, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit, URL_ENDPOINT
import shutil
import uuid
import os
import tempfile
from app.users import auth_backend, fastapi_users, current_active_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

@app.post("/upload")
async def upload_file(
    file : UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
    ):

    temp_file_path = None

    try:  

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        with open(temp_file_path, "rb") as f:
            upload_result = imagekit.files.upload(
                file=f,
                file_name=file.filename,
                use_unique_file_name=True,
                tags=["backend-upload"],
            )

        if upload_result:

            post = Post(
                user_id=user.id,
                caption=caption,
                url=upload_result.url,
                title="dummy title",
                file_type=file.content_type,
                file_name=upload_result.name,
                file_id=upload_result.file_id
            )

            session.add(post)
            await session.commit()
            await session.refresh(post)

            return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)  # Delete the temporary file after upload
        file.file.close()  # Close the file after processing
    
@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
    ):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        post_data = {
            "id": str(post.id),
            "user_id": str(post.user_id),
            "caption": post.caption,
            "url": post.url,
            "title": post.title,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat(),
            "is_owner": user.id == post.user_id
        }
        posts_data.append(post_data)

    return {"posts": posts_data}

@app.delete("/delete/{post_id}")
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
    ):
    try:
        post_uuid = uuid.UUID(post_id)  # Convert the string to a UUID object

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Delete the file from ImageKit
        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="You are not the owner of this post")
        imagekit.files.delete(post.file_id)

        # Delete the post from the database
        await session.delete(post)
        await session.commit()

        return {"message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))