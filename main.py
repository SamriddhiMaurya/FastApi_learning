from fastapi import FastAPI , HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Hello World"}



#dynamic routes

@app.get("/items/{item_id}")
def items(item_id):
    return {"itemm_id": item_id}

users=[]
#pydantic models
class User(BaseModel):
    name: str
    age: int
    email: str
 
 
    
@app.post("/create_users")
def create_user(user: User):
    users.append(user)
    return {"message": "User created successfully!", "data": user}

@app.get("/get_users")
def get_users():
    return {"message": "List of users", "data": users}


class Userr(BaseModel):
    name: str
    age: int
    passkey: int


#response model

class UserResponse(BaseModel):
    name: str
    age: int
    
@app.get("/new_user", response_model=UserResponse)
def get_user():
    return {
        "name": "John Doe",
        "age": 30,      
        "passkey": 12345
    }
    



#status code and responses

#exceptional handelling 



#custom exception
class UserNotFoundException(Exception):
    def __init__(self, name:str):
        self.name = name
        
        
@app.exception_handler(UserNotFoundException)
def user_not_found_handeller(request:Request, exc:UserNotFoundException ):
    return JSONResponse(
        status_code=404, 
        content={
            "status":"error", 
            "message":f"User {exc.name} not found"
        }
    )
    

@app.get("/user/{name}")
def get_user(name:str):
    if name != "samriddhi":
        raise UserNotFoundException(name)
    return{
        "name":name
    }
    
    
    
