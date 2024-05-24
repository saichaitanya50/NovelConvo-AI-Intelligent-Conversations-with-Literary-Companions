import re
import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
        Write the code in such a way that it can be re-used for processing the user's query.
        To be implemented."""
        
        text = text.lower()
        cleaned_text = re.sub(r'[—]', ' ', text)
        cleaned_text = re.sub(r'[-]', ' ', cleaned_text)
        cleaned_text = re.sub(r'[–]', ' ', cleaned_text)
        cleaned_text = re.sub(r'[‐]', ' ', cleaned_text)
        cleaned_text = re.sub(r'[/]', ' ', cleaned_text)
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        tokens = cleaned_text.split(' ')
        
        terms = []
        for token in tokens:
            if (token not in self.stop_words) and (token != ' '):
                terms.append(self.ps.stem(token))
        return terms