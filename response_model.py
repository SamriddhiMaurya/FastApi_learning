from fastapi import FastAPI
from pydantic import BaseModel


app  = FastAPI()



class User(BaseModel):
    name: str
    age: int
    passkey: int


#response model

class UserResponse(BaseModel):
    name: str
    age: int
    
@app.get("/user", response_model=UserResponse)
def get_user():
    return {
        "name": "John Doe",
        "age": 30,      
        "passkey": 12345
    }