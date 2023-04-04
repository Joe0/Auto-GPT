import snapshots

message_history = []

def append(message):
    message_history.append(message)
    if not snapshots.create_snapshot():
        print("Failed to persist message history")
        del message_history[-1]
        return None
    return message

def get_history():
    return message_history

def set_history(history):
    global message_history
    message_history = history
