from tqdm import tqdm
from .preprocessor import Preprocessor
from .indexer import Indexer
from collections import OrderedDict
from .linkedlist import LinkedList
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()
    
    def _merge(self, posting_list_1, posting_list_2, skip):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
            
        result = LinkedList()
        comparisons_count = 0
        if skip:
            ptr1 = posting_list_1.start_node
            ptr2 = posting_list_2.start_node
            while ptr1 != None and ptr2 != None:
                if ptr1.value == ptr2.value:
                    result.insert_at_end(ptr1.value)
                    ptr1 = ptr1.next
                elif ptr1.value < ptr2.value:
                    if ptr1.skip:
                        if ptr1.skip.value < ptr2.value:
                            ptr1 = ptr1.skip
                        else:
                            ptr1 = ptr1.next
                    else:
                        ptr1 = ptr1.next
                    comparisons_count += 1
                else:
                    if ptr2.skip:
                        if ptr2.skip.value < ptr1.value:
                            ptr2 = ptr2.skip
                        else:
                            ptr2 = ptr2.next
                    else:
                        ptr2 = ptr2.next
                    comparisons_count += 1
            result.add_skip_connections()
        else:
            ptr1 = posting_list_1.start_node
            ptr2 = posting_list_2.start_node
            while ptr1 != None and ptr2 != None:
                if ptr1.value == ptr2.value:
                    result.insert_at_end(ptr1.value)
                    ptr1 = ptr1.next
                elif ptr1.value < ptr2.value:
                    ptr1 = ptr1.next
                    comparisons_count += 1
                else:
                    ptr2 = ptr2.next
                    comparisons_count += 1
        
        return result, comparisons_count

    def _daat_and(self, query_terms, skip=False, tf_idf=False):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        posting_lists = []
        for query_term in query_terms:
            try:
                posting_lists.append(self.indexer.get_index()[query_term])
            except KeyError:
                posting_lists.append(LinkedList())
        
        sorted_posting_lists = sorted(posting_lists, key=lambda x: x.length)
        result = sorted_posting_lists[0]
        comparisons_count = 0
        for posting_list in sorted_posting_lists[1:]:
            result, temp_comparisons_count = self._merge(result, posting_list, skip)
            comparisons_count += temp_comparisons_count
        
        result = result.traverse_list()
        if tf_idf:
            tf_idf_scores = {}
            for doc_id in result:
                if doc_id not in tf_idf_scores.keys():
                    tf_idf_scores[doc_id] = []
                for query_term in query_terms:
                    tf_idf_scores[doc_id].append(self.indexer.tf_idf[query_term][doc_id])
            
            tf_idf_max = {}
            for doc_id in tf_idf_scores.keys():
                tf_idf_max[doc_id] = max(tf_idf_scores[doc_id])
            
            result = sorted(result, key=lambda x: tf_idf_max[x], reverse=True)

        
        return result, comparisons_count, len(result)

    def _get_postings(self, term):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        ps_list = self.indexer.get_index()[term]
        return ps_list

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        docs = {}
        with open(corpus, 'r') as fp:
            for line in tqdm(fp.readlines()):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                docs[doc_id] = tokenized_document
        doc_ids = list(docs.keys())
        doc_ids.sort()
        for doc_id in doc_ids:
            self.indexer.generate_inverted_index(doc_id, docs[doc_id])
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf()

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}
        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""
            input_term_arr = self.preprocessor.tokenizer(query)  # Tokenized query. To be implemented.
            for term in input_term_arr:
                postings, skip_postings = None, None

                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""
                try:
                    ps_list = self._get_postings(term)
                    postings = ps_list.traverse_list()
                    skip_postings = ps_list.traverse_skips()
                    output_dict['postingsList'][term] = postings
                    output_dict['postingsListSkip'][term] = skip_postings
                except KeyError:
                    output_dict['postingsList'][term] = []
                    output_dict['postingsListSkip'][term] = []
            
            
            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            and_comparisons_no_skip, and_comparisons_skip, \
                and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None, None, None
            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)
            
            and_op_no_score_no_skip, and_comparisons_no_skip, and_results_cnt_no_skip = self._daat_and(input_term_arr)
            
            and_op_no_score_skip, and_comparisons_skip, and_results_cnt_skip = self._daat_and(input_term_arr, skip=True)
            
            and_op_no_score_no_skip_sorted, and_comparisons_no_skip_sorted, and_results_cnt_no_skip_sorted = self._daat_and(input_term_arr, tf_idf=True)
            
            and_op_no_score_skip_sorted, and_comparisons_skip_sorted, and_results_cnt_skip_sorted = self._daat_and(input_term_arr, skip=True, tf_idf=True)
            
            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here")

    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9999)
