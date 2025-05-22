from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from database import get_db
from models import User

app = FastAPI()

@app.post("/create_user")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.delete("/delete_user")
def delete_user(username:str, password: str, db : Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Username does not exist")
    if existing_user.password != password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    db.delete(existing_user)
    db.commit()

    return {"message": "User deleted successfully"}

@app.get("/list_users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.put("/update_password")
def update_password(username: str, old_password: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.password != old_password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    user.password = new_password
    db.commit()
    db.refresh(user)

    return {"message": "Password updated successfully"}

