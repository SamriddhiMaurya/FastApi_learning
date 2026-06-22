from fastapi import FastAPI , Depends, Header  , HTTPException , Request #header for auth
from pydantic import BaseModel
import time #for middleware
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
    





#dependency injection 
#commom logic

def common_logic():
    return{
        "message":"common logic executed"
    } 


@app.get("/home")
def homee(data=Depends(common_logic)):
    return data


#reusable logic of dependency injection 

def get_current_user():
    return{
        "user": "Sam"
    }
    
@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return user 

@app.get("/dashboard")
def dashboard(user = Depends(get_current_user)):
    return user 



#Auth


def verify_token(token: str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(
            status_code=401,
            detail="unauthorized"
        )
    return {
        "user": "Authorized User"
    }
    
@app.get("/secure-data")
def secure_data(user=Depends(verify_token)):
    return {
        "message": "secure data accessed",
        "user": user
    }
    
    
    
#middleware 


@app.middleware("http")
# async def my_middleware(request: Request, call_next):
#     print("Request Received")
#     response= await call_next(request)
#     print("response sent")
#     return response


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start_time=time.time()
    
    response = await call_next(request)
    
    process_time = time.time()-start_time
    
    print(f"Path:{request.url.path} | Time:{process_time}")
    
    return response