from datetime import datetime


class KeyElement:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.list_of_index_next_node = None
        self.list_of_index_prev_node = None
        self.lru_queue_next_node = None
        self.lru_queue_prev_node = None
        self.date_and_time = None
        self.date_and_time_string = None
        self.update_date_and_time()

    def update_key(self, value):
        self.value = value
        self.update_date_and_time()

    def update_date_and_time(self):
        self.date_and_time = datetime.now()
        self.date_and_time_string = self.date_and_time.strftime("%Y-%m-%d %H:%M:%S")


