import sqlite3
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import Column, Integer, String

app=FastAPI()
conn =  sqlite3.connect("test.db" , check_same_thread= False)

cursor = conn.cursor() 

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    title TEXT,
    completed TEXT
    )             
""")

conn.commit()  #to save the changes 


@app.get("/")
def home():
    return{
        "message":"SQLLite connected."
    }
    
    
    
#SQLAlchemy Database


DATABASE_URL = "sqlite:///./test.db"


#databse connection using engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread":False}
)

#sessionLocal helps db to know that operitaions can be performed in db
sessionLocal = sessionmaker(bind=engine)


#base is used to act as a base for model
Base = declarative_base()


class Todo(Base):
    __tablename__="todos"
    
    id= Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)
    
Base.metadata.create_all(bind = engine)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
        


#create API
@app.post("/todos")
def create_todo(title:str , db:Session = Depends(get_db)):
    todo = Todo(title=title, completed="False")
    db.add(todo) #adding to db
    db.commit() #saving to db
    db.refresh(todo) #refreshing the db
    return{
        "message":"Todo Created" , 
        "data":todo
    }
    
    
#READ ALL DATA

@app.get("/todos")
def get_todos(db:Session=Depends(get_db)):
    todos=db.query(Todo).all()
    
    return{
        "Total":len(todos), 
        "data": todos
    }
    
    
@app.get("/todos/{todo_id}")
def get_todo(todo_id = int , db : Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code = 404, deatail="Todo not found")
    return todo


#Update Data in DB

@app.put("/todos/{todo_id}")
def update_todo(todo_id:int , title:str , db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id ==  todo_id).first()
    
    if not todo:
        raise HTTPException(status_code = 404, deatail="Todo not found")
    
    
    todo.title = title 
    
    db.commit()
    db.refresh(todo)
    
    return {
        "message": "todo title updates", 
        "data":todo
    }
    
    
    #delete operation
    

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int , db:Session=Depends(get_db)):
    todo= db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code = 404, deatail="Todo not found")
    
    db.delete(todo)
    db.commit()
    
    return{"message":"deleted"}

