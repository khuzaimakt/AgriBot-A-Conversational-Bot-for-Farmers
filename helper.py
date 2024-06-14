import os
from pathlib import Path
import shutil
from fastapi import UploadFile



def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def get_next_file_number(directory_path):
    existing_files = [f for f in os.listdir(directory_path) if f.endswith('.mp3')]
    if not existing_files:
        return 1
    existing_numbers = [int(f.split('.')[0]) for f in existing_files]
    return max(existing_numbers) + 1

def store_output_audio_file(user_id, session_id, mp3_content):
    cwd = os.getcwd()
    input_audio_path = os.path.join(cwd, 'input_audio')
    user_path = os.path.join(input_audio_path, str(user_id))
    session_path = os.path.join(user_path, str(session_id))

    # Ensure the directories exist
    ensure_directory_exists(input_audio_path)
    ensure_directory_exists(user_path)
    ensure_directory_exists(session_path)

    # Get the next file number
    next_file_number = get_next_file_number(session_path)
    new_file_path = os.path.join(session_path, f"{next_file_number}.mp3")

    # Save the new file
    with open(new_file_path, 'wb') as file:
        file.write(mp3_content)

    print(f"Stored {new_file_path}")


def get_store_input_path(user_id, session_id):
    cwd = os.getcwd()
    input_audio_path = os.path.join(cwd, 'input_audio')
    user_path = os.path.join(input_audio_path, str(user_id))
    session_path = os.path.join(user_path, str(session_id))

    # Ensure the directories exist
    ensure_directory_exists(input_audio_path)
    ensure_directory_exists(user_path)
    ensure_directory_exists(session_path)

    # Get the next file number
    next_file_number = get_next_file_number(session_path)
    new_file_name = f"{next_file_number}.mp3"
    new_file_path = os.path.join(session_path, new_file_name)

    return new_file_path

    # Move and rename the file
    with open(new_file_path, "wb") as buffer:
        shutil.copyfileobj(mp3_file.file, buffer)

    print(f"Stored {new_file_path}")
    mp3_file.file.close()


def get_store_output_path(user_id, session_id):
    cwd = os.getcwd()
    input_audio_path = os.path.join(cwd, 'output_audio')
    user_path = os.path.join(input_audio_path, str(user_id))
    session_path = os.path.join(user_path, str(session_id))

    # Ensure the directories exist
    ensure_directory_exists(input_audio_path)
    ensure_directory_exists(user_path)
    ensure_directory_exists(session_path)

    # Get the next file number
    next_file_number = get_next_file_number(session_path)
    new_file_name = f"{next_file_number}.mp3"
    new_file_path = os.path.join(session_path, new_file_name)

    return new_file_path


