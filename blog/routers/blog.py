from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import UploadFile, File
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

get_db = database.get_db


@router.post("/upload/")
async def create_upload_file(request):
    print('--------')
    # print("video", video)
    print("request", request)
    return {"filename": 'video'}


@router.get('/')
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    # res = []
    # for blog in blogs:
    #     item = {"title": blog.title, "id": blog.id}
    #     res.append(item)
    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(
        # video: UploadFile,
        request: schemas.BlogBase,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)
):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    item = db.query(models.Blog).filter(models.Blog.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update the item attributes with the non-None values from the request
    for key, value in request.dict(exclude_unset=True).items():
        if value is not None:
            setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return request.dict(exclude_unset=True).items()


@router.get('/{id}', status_code=200)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
    return blog
