from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from config import engine, Base, get_db
import models
import crud
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import requests
import torch
import os
import json
import requests
import gtts
from llm import Chatbot
from pathlib import Path
import shutil
from helper import get_store_input_path, get_store_output_path

os.getcwd()

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

API_URL_STT = (
    "https://api-inference.huggingface.co/models/khuzaimakt/whisper-small-ur-kt"
)
headers_STT = {"Authorization": "Bearer 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"}


# User endpoints
@app.post("/users/", response_model=crud.UserResponse)
async def create_user(user: crud.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.phoneno == user.phoneno).first()
    if db_user:
        return db_user
    db_user = crud.create_user(db=db, user=user)

    return db_user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"}


# ChatSession endpoints
@app.post("/sessions/", response_model=crud.ChatSessionCreate)
async def create_chat_session(
    session: crud.ChatSessionCreate, db: Session = Depends(get_db)
):
    return crud.create_chat_session(db=db, session=session)


@app.post("/sessions/user_id")
async def read_chat_session(user: crud.ReadChatSession, db: Session = Depends(get_db)):
    db_session = crud.get_chat_sessions(db=db, user_id=user.user_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Chat session not found")

    ids = [session.id for session in db_session]
    session_names = [session.session_name for session in db_session]

    return {"ids": ids, "session_names": session_names}


@app.delete("/sessions/{session_id}")
async def delete_chat_session(session_id: int, db: Session = Depends(get_db)):
    db_session = crud.get_chat_session(db=db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Chat session not found")
    crud.delete_chat_session(db=db, session_id=session_id)
    return {"message": "Chat session deleted successfully"}


@app.post("/messages/get_messages")
async def read_message(user: crud.ReadMessage, db: Session = Depends(get_db)):
    db_message = crud.get_messages(
        db=db, user_id=user.user_id, session_id=user.session_id
    )
    if db_message is None:
        raise HTTPException(status_code=404, detail="Messages not found")

    queries = [session.query for session in db_message]
    responses = [session.response for session in db_message]
    query_audios = [session.query_audio for session in db_message]
    response_audios = [session.response_audio for session in db_message]

    return {
        "queries": queries,
        "responses": responses,
        "query_audios": query_audios,
        "response_audios": response_audios,
    }


@app.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.get_message(db=db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    crud.delete_message(db=db, message_id=message_id)
    return {"message": "Message deleted successfully"}


@app.post("/Speech-To-Text/")
async def speech_to_text(query_audio: UploadFile = File(...)):
    contents = await query_audio.read()  # Read the contents of the uploaded file

    response = requests.post(API_URL_STT, headers=headers_STT, data=contents)

    output = response.json()
    return output["text"]


@app.post("/messages/create_message")
async def create_message(
    user: crud.CreateMessage,
    db: Session = Depends(get_db),
):

    def read_preprompts(filename: str):
        def parse(data):
            prompts = []
            for item in data:
                prompts.append(
                    "\n".join(
                        [indiv.strip() for indiv in item.split("\n") if indiv.strip()]
                    )
                )
            return prompts

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return parse(data)

    preprompts = read_preprompts("preprompts_en.json")

    chatbot = Chatbot(preprompts, "ur", "en")

    model_answer, translated_answer = chatbot.execute_pipeline(user.query)

    
    db_message = crud.create_message(
        db=db,
        user_id=user.user_id,
        session_id=user.session_id,
        query=user.query,
        response=translated_answer,
        
    )
    if db_message is None:
        raise HTTPException(status_code=404, detail="Messages not found")

    
    return translated_answer


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
