from KeyElement import KeyElement


class HashTableIndex:
    def __init__(self):
        self.head_list_of_index = None

    def add_to_list_of_index(self, new_key_element: KeyElement):
        new_key_element.list_of_index_next_node = self.head_list_of_index
        if self.head_list_of_index is not None:
            self.head_list_of_index.list_of_index_prev_node = new_key_element
        self.head_list_of_index = new_key_element

    def update_list_of_index(self, key_element: KeyElement):
        if self.head_list_of_index == key_element: return
        key_element.list_of_index_prev_node.list_of_index_next_node = key_element.list_of_index_next_node
        if key_element.list_of_index_next_node is not None:
            key_element.list_of_index_next_node.list_of_index_prev_node = key_element.list_of_index_prev_node
        key_element.list_of_index_next_node = self.head_list_of_index
        key_element.list_of_index_prev_node = None
        self.head_list_of_index.list_of_index_prev_node = key_element
        self.head_list_of_index = key_element
