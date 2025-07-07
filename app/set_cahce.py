from collections import OrderedDict

qa_cache = OrderedDict()

def set_cache(session_id, qa_chain, max_session):
    if session_id in qa_cache:
        qa_cache.move_to_end(session_id)
    elif len(qa_cache) >= max_session:
        remove_id = qa_cache.popitem(last=False)
        print(f"Oldest session {remove_id} removed!")
        qa_cache[session_id] = qa_chain

def get_cache(session_id):
    return qa_cache[session_id]

def is_cache(session_id):
    return session_id in qa_cache


