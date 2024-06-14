from sqlalchemy.orm import Session
from models import User, ChatSession, Message
from pydantic import BaseModel

# Pydantic models
class UserCreate(BaseModel):
    phoneno: str

class UserResponse(BaseModel):
    id:int

class ChatSessionCreate(BaseModel):
    user_id: int
    session_name: str

class MessageCreate(BaseModel):
    user_id: int
    session_id: int
    query: str
    response: str
    query_audio: str
    response_audio: str

class MessageResponse(BaseModel):
    query: str
    response: str
    query_audio: str
    response_audio: str

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()



def create_user(db: Session, user: UserCreate):
    db_user = User(phoneno=user.phoneno)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# ChatSession CRUD operations
def get_chat_sessions(db: Session, user_id: int):
    return db.query(ChatSession).filter(ChatSession.user_id == user_id).all()

def get_chat_session(db: Session, session_id:int):
    return db.query(ChatSession).filter(ChatSession.id ==session_id).first()


def create_chat_session(db: Session, session: ChatSessionCreate):
    db_session = ChatSession(user_id=session.user_id, session_name=session.session_name)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def delete_chat_session(db: Session, session_id: int):
    db_session = get_chat_session(db, session_id)
    if db_session:
        db.delete(db_session)
        db.commit()
    return db_session

# Message CRUD operations
def get_messages(db: Session, user_id: int,session_id:int):
    return db.query(Message).filter(Message.user_id == user_id and Message.session_id==session_id).all()

def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()

def create_message(db: Session,user_id:int,session_id:int,query:str,response:str,query_audio:str,response_audio:str):
    db_message = Message(
        user_id=user_id,
        session_id=session_id,
        query= query,
        response= response,
        query_audio= query_audio,
        response_audio= response_audio
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def delete_message(db: Session, message_id: int):
    db_message = get_message(db, message_id)
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message
