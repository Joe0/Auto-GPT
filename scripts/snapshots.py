import time
import os
import shelve
import message_history
import memory
from config import Config

cfg = Config()

def persist_message_history(current_unix_time):
    os.makedirs(f"outputs/snapshots/{current_unix_time}", exist_ok=True)
    with shelve.open(f"outputs/snapshots/{current_unix_time}/store") as f:
        f["message_history"] = message_history.get_history()
    return True

def load_message_history(file):
    try:
        with shelve.open(file) as f:
            global message_history
            message_history.set_history(f["message_history"])
        print("Loaded message history")
        return True
    except Exception as e:
        print("Failed to load message history")
        print(e)
        return False

def persist_memory(current_unix_time):
    os.makedirs(f"outputs/snapshots/{current_unix_time}", exist_ok=True)
    with shelve.open(f"outputs/snapshots/{current_unix_time}/store") as f:
        f["memory"] = memory.permanent_memory
    return True

def load_memory(file):
    try:
        with shelve.open(file) as f:
            memory.permanent_memory = f["memory"]
        print("Loaded memory")
        return True
    except Exception as e:
        print("Failed to load memory")
        print(e)
        return False
    
def create_snapshot():
    if not cfg.snapshots_enabled:
        return True
    current_unix_time = int(time.time())
    return persist_message_history(current_unix_time) and persist_memory(current_unix_time)

def load_snapshot(file):
    return load_message_history(file) and load_memory(file)
