from datetime import datetime

from HashTableIndex import HashTableIndex
from KeyElement import KeyElement


class TimeBasedLruCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.hashTabel = [HashTableIndex() for _ in range(capacity)]
        self.num_of_elements = 0
        self.lru_queue_head = None
        self.tail = None

    def put(self, key, value):
        current = self.find_place_in_cache(key)

        if self.is_new_key(current):
            if self.is_full():
                self.remove_oldest_element()

            current = KeyElement(key, value)
            index = self.hash_function(key)
            self.hashTabel[index].add_to_list_of_index(current)
            self.add_to_lru_queue(current)
            self.num_of_elements += 1

        else:  # The key already exist in the cache, so it will be updated
            index = self.hash_function(key)
            current.update_key(value)
            current.update_date_and_time()
            self.update_lru_queue(current)
            self.hashTabel[index].update_list_of_index(current)

    def get(self, key):
        current = self.search_key(key)
        index = self.hash_function(key)

        if current is None:
            return None
        else:
            current.update_date_and_time()
            self.update_lru_queue(current)
            self.hashTabel[index].update_list_of_index(current)
            return current.value

    def clear_expired(self, seconds):
        expired_key = self.search_expired_key(seconds)

        while expired_key:
            self.remove(expired_key.key)
            expired_key = expired_key.lru_queue_next_node

    def print_cache(self):
        if self.is_empty():
            print("The cache is empty")
        else:
            print("The cache:")
            print("Index      | Elements")
            for i in range(self.capacity):
                print(f"{i}".ljust(len("Index      "), " ") + "|", end="")
                temp = self.hashTabel[i].head_list_of_index
                while temp:
                    print(f"{temp.key}: {temp.value} {temp.date_and_time_string}", end="")
                    temp = temp.list_of_index_next_node
                    if temp:
                        print("     -->     ", end="")
                print()
        self.print_lru_queue()

    def print_lru_queue(self):
        temp = self.lru_queue_head
        if self.is_empty():
            print("The cache is empty and therefore there is no LRU queue")
        else:
            print("\nThe LRU queue:")
        while temp:

            print(f"{temp.key} : {temp.value} {temp.date_and_time_string}")
            temp = temp.lru_queue_next_node
            if temp:
                print(" " * 15 + "|\n" + " " * 15 + "▼")
        print()

    def update_lru_queue(self, keyElement):
        if keyElement == self.lru_queue_head:
            return
        if keyElement == self.tail:
            keyElement.lru_queue_prev_node.lru_queue_next_node = None
            self.tail = keyElement.lru_queue_prev_node
            keyElement.lru_queue_prev_node = None
            keyElement.lru_queue_next_node = self.lru_queue_head
            self.lru_queue_head.lru_queue_prev_node = keyElement
            self.lru_queue_head = keyElement
            return

        keyElement.lru_queue_prev_node.lru_queue_next_node = keyElement.lru_queue_next_node
        keyElement.lru_queue_next_node.lru_queue_prev_node = keyElement.lru_queue_prev_node
        keyElement.lru_queue_prev_node = None
        keyElement.lru_queue_next_node = self.lru_queue_head
        self.lru_queue_head.lru_queue_prev_node = keyElement
        self.lru_queue_head = keyElement

    def add_to_lru_queue(self, keyElement):
        if self.lru_queue_head is None:
            self.lru_queue_head = keyElement
            self.tail = keyElement
        else:
            keyElement.lru_queue_next_node = self.lru_queue_head
            self.lru_queue_head.lru_queue_prev_node = keyElement
            self.lru_queue_head = keyElement

    def remove_from_lru_queue(self, keyElement):
        if self.lru_queue_head == keyElement:
            self.lru_queue_head = keyElement.lru_queue_next_node
        if self.tail == keyElement:
            self.tail = keyElement.lru_queue_prev_node
        if keyElement.lru_queue_prev_node:
            keyElement.lru_queue_prev_node.lru_queue_next_node = keyElement.lru_queue_next_node
        if keyElement.lru_queue_next_node:
            keyElement.lru_queue_next_node.lru_queue_prev_node = keyElement.lru_queue_prev_node

    def hash_function(self, key):
        if key is None:
            return None
        return abs(hash(key)) % self.capacity

    def remove(self, key):
        index = self.hash_function(key)

        current = self.hashTabel[index].head_list_of_index
        while current and current.key != key:
            current = current.list_of_index_next_node

        if current is None:
            print("Key does not exist")
        else:
            self.remove_from_lru_queue(current)
            if self.hashTabel[index].head_list_of_index == current:
                self.hashTabel[index].head_list_of_index = current.list_of_index_next_node
            if current.list_of_index_prev_node:
                current.list_of_index_prev_node.list_of_index_next_node = current.list_of_index_next_node
            if current.list_of_index_next_node:
                current.list_of_index_next_node.list_of_index_prev_node = current.list_of_index_prev_node
            self.num_of_elements -= 1

    def find_place_in_cache(self, key):
        index = self.hash_function(key)
        current = self.hashTabel[index].head_list_of_index
        while current and current.key != key:
            current = current.list_of_index_next_node
        return current

    def remove_oldest_element(self):
        self.remove(self.tail.key)

    def is_full(self):
        return self.num_of_elements == self.capacity

    def is_empty(self):
        return self.num_of_elements == 0

    def search_key(self, key):
        index = self.hash_function(key)
        current = self.hashTabel[index].head_list_of_index
        while current and current.key != key:
            current = current.list_of_index_next_node
        return current

    def search_expired_key(self, seconds):
        current = self.lru_queue_head
        current_time = datetime.now()
        while current and self.time_difference_in_seconds(current.date_and_time, current_time) <= seconds:
            current = current.lru_queue_next_node
        return current

    def is_new_key(self, current):
        return current is None

    def time_difference_in_seconds(self, time1, time2):
        return abs(int((time2 - time1).total_seconds()))
