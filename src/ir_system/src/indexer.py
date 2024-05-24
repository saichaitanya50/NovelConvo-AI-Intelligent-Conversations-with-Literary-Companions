from .linkedlist import LinkedList
from collections import OrderedDict


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.total_docs = set()
        self.tf = {}
        self.tf_idf = {}

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        self.total_docs.add(doc_id)
        for t in tokenized_document:
            if t not in self.tf.keys():
                self.tf[t] = {}
            if doc_id not in self.tf[t].keys():
                self.tf[t][doc_id] = 0
            
            self.tf[t][doc_id] += 1
            self.add_to_index(t, doc_id)
            
        for t in tokenized_document:
            self.tf[t][doc_id] /= len(tokenized_document)

    def add_to_index(self, term_, doc_id_):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
        try:
            if self.inverted_index[term_].end_node.value != doc_id_:
                self.inverted_index[term_].insert_at_end(doc_id_)
        except KeyError:
            self.inverted_index[term_] = LinkedList()
            self.inverted_index[term_].insert_at_end(doc_id_)

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        for term in self.inverted_index.keys():
            self.inverted_index[term].add_skip_connections()

    def calculate_tf_idf(self):
        for term in self.inverted_index.keys():
            try:
                idf = len(self.total_docs)/self.inverted_index[term].length
            except ZeroDivisionError:
                idf = 0
            if term not in self.tf_idf.keys():
                self.tf_idf[term] = {}
            for doc_id in self.inverted_index[term].traverse_list():
                if doc_id not in self.tf_idf[term].keys():
                    self.tf_idf[term][doc_id] = 0
                self.tf_idf[term][doc_id] = self.tf[term][doc_id]*idf