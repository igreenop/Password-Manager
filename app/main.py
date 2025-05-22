from fastapi import FastAPI, HTTPException

app = FastAPI()

users = {}

@app.get("/")
def read_root():
    return {"message": "Hello World :D"}

@app.post("/create_user")
def create_user(username: str, password: str):
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[username] = password
    return {"message": "User created successfully"}

@app.delete("/remove_user")
def remove_user(username: str, password: str):
    if username not in users:
        raise HTTPException(status_code=400, detail="User does not exist")
    if password != users[username]:
        raise HTTPException(status_code=400, detail="Incorrect password")
    result = users.pop(username)
    return {"message": "User deleted successfully"}
