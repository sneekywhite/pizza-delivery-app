from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas,models
from .database import engine, sessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags=['Blog'])
def create(request: schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title =request.title, body =request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def delete_blog(id, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")  
    blog.delete(synchronize_session=False)
    db.commit()
    return f"blog with id {id} has been deleted"


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def update_blog(id, request: schemas.Blog, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")
    blog.update({'title': request.title, 'body':request.body})
    db.commit()
    return 'updated'



@app.get('/get_blog', tags=['Blog'])
def get_all_blog(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['Blog'])
def get_single_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'detail': f"Blog with the id {id} is not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    
    return blog



@app.post('/user', response_model=schemas.Show_user, tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name =request.name, email=request.email, password=Hash.bycrpt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.Show_user, tags=['User'])
def get_user(id:int, db:Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    return user

