import sqlite3
from fastapi import FastAPI, Depends
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
        
@app.get("/")
def home(db:Session = Depends(get_db)):
    return{
        "message":"DB connected file"
    }

