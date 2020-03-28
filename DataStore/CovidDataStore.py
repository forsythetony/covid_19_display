import threading

class CovidDataStore():
    
    def __init__(self):
        self._messages = []
        self._lock = threading.Lock()

    def get_messages(self):
        with self._lock:
            return self._messages

    def get_total_message_count(self):
        with self._lock:
            return len(self._messages)

    def clear_messages(self):
        with self._lock:
            self._messages.clear()
    
    def get_message_for_index(self, index):
        with self._lock:

            messages_length = len(self._messages)

            if messages_length == 0:
                return None
            
            index_to_grab = index % messages_length

            return self._messages[index_to_grab]

    def add_message(self, message):
        with self._lock:
            self._messages.append(message)

    def add_messages(self, messages, clear):
        with self._lock:
            if clear:
                self._messages.clear()

            self._messages.extend(messages)