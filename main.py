from fastapi import FastAPI , Depends, Header  , HTTPException  #header for auth
app = FastAPI()




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
    
    
    
