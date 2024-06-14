from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True)
    phoneno = Column(String, unique=True, index=True, nullable=False)
    chat_sessions = relationship("ChatSession", back_populates="user")
    messages = relationship("Message", back_populates="user")

class ChatSession(Base):
    __tablename__ = 'ChatSessions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    session_name = Column(Text, nullable=False)
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = 'Messages'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    session_id = Column(Integer, ForeignKey('ChatSessions.id'), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    query_audio = Column(Text, nullable=True, default=None)  # Default set to None
    response_audio = Column(Text, nullable=False)
    user = relationship("User", back_populates="messages")
    session = relationship("ChatSession", back_populates="messages")
