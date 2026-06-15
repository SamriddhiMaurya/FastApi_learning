from fastapi import FastAPI , status , HTTPException
from pydantic import BaseModel
app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Hello World"}



#dynamic routes

@app.get("/items/{item_id}")
def items(item_id: int):
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

@app.post("/create_userr", status_code=status.HTTP_201_CREATED)
def create_userr():
    return{
        "message":"User Created"
    }
    
    
    
#custom_response
@app.get("/userr")
def get_custom_userr():
    return {"message": "This is a custom user response",
            "status": "Success", 
            "data":{
                "name":"sam"
            }
        }




@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="user not found")
    return {"user_id": 1, "name": "sam"}

 