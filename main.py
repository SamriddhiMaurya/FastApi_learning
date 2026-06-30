from fastapi import FastAPI , HTTPException, Depends , Header
from jose import jwt
from datetime import datetime, timedelta, timezone


app=FastAPI()

SECRET_KEY = "mysecret"

ALGORITHM = "HS256"

#create token 
def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    
    return token


#login API(Token Generation)
@app.post("/login")
def login(usernname:str, password:str):
    if usernname != "admin" or password != "1234":
        raise HTTPException(
            status_code=401, 
            datail  = "Invalid Username and password"
        )
    token = create_token({
        "sub":usernname
    })
    return{
        "access_token":token
    }
    
    
#token verify

def verify_token(token: str = Header(None)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )
        
        
        
#protected route

@app.get("/secure")
def secure_data(user = Depends(verify_token)):
    return{
        "mesaage": "Secure data accessed", 
        "user":user
    }