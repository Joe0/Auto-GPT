import snapshots

permanent_memory = []

def commit_memory(string):
    permanent_memory.append(string)
    snapshots.create_snapshot()
    return True

def delete_memory(key):
    if key in permanent_memory:
        del permanent_memory[key]
        snapshots.create_snapshot()
        return key
    else:
        return None

def overwrite_memory(key, string):
    if key in permanent_memory:
        permanent_memory[key] = string
        snapshots.create_snapshot()
        return key
    else:
        return None

def clear_memory():
    permanent_memory.clear()
    snapshots.create_snapshot()
    return True
