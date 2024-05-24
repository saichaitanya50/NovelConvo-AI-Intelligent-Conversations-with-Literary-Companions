import math

class Node:

    def __init__(self, value=None, next=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.skip = None


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length = 0 
        
        self.skip_length = None
        self.n_skips = 0
        self.has_skips = False
        
        
        self.idf = 0.0

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return traversal
        else:
            node = self.start_node
            while node != None:
                traversal.append(node.value)
                node = node.next
            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return traversal
        else:
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            if not self.has_skips:
                return []
            
            node = self.start_node
            while node != None:
                traversal.append(node.value)
                node = node.skip
            return traversal

    def add_skip_connections(self):
        self.n_skips = math.floor(math.sqrt(self.length))
        if self.n_skips * self.n_skips == self.length:
            self.n_skips = self.n_skips - 1
        self.skip_length = round(math.sqrt(self.length))
        """ Write logic to add skip pointers to the linked list. 
            This function does not return anything.
            To be implemented."""
        skip_len_counter = 0
        if self.start_node is None:
            return
        else:
            node = self.start_node
            skip_node_tracker = node
            while node != None:
                if skip_len_counter % self.skip_length == 0 and skip_len_counter != 0:
                    skip_node_tracker.skip = node
                    skip_node_tracker = node
                    self.has_skips = True
                node = node.next
                skip_len_counter += 1
            return
        

    def insert_at_end(self, value):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """
        if self.start_node == None:
            self.start_node = Node(value)
            self.end_node = self.start_node
            self.length += 1
        else:
            self.end_node.next = Node(value)
            self.end_node = self.end_node.next
            self.length += 1

