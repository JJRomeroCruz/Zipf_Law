import fitz
import re
import pandas as pd
import nltk
from collections import Counter

class document:
    def __init__(self, path):
        self.path = path

    def get_doc(self):
        """
        Args: 
            document
        Returns: 
            the document itself
        """
        return fitz.open(self.path)
    
    def get_text_pages(self):
        """
        Args: 
            document
        Returns:  
            output: list of str, the list in which each element is a page
        """
        doc = fitz.open(self.path)
        output = []
        for page in doc:
            # lower
            page.lower()
            
            # remove characters that are not numbers or letters
            re.sub('[^A-Za-z0-9]+', '', page)

            output.append(page)
        return output
    
    def get_text_sent(self):
        """
        Args: 
            document
        Returns: 
            output: str, a list of str by sentences
        """
        doc = fitz.open(self.path)
        output = []
        for page in doc:
            text = page.get_text()
            text.lower()
            re.sub('[^A-Za-z0-9]+', '', text)
            output.append(text)
        return nltk.tokenize.sent_tokenize(output, language='spanish')
    
    def get_text_word(self):
        """
        Args: 
            document

        Return: 
            list of text tokenized by words
        """
        doc = fitz.open(self.path)
        output = []
        for page in doc: 
            text = page.get_text()
            text.lower()
            re.sub('[^A-Za-z0-9]+', '', text)
            output.append(text)
        return nltk.tokenize.word_tokenize(output, language='spanish')
    
    def get_pages(self):
        """
        Args:
            document
        Returns: 
            pages: float, the number of pages
        """
        doc = fitz.open(self.path)
        return len(doc)
    
    def count_words(self):
        """
        Args: 
            document
        Returns: 
            v_sorted: dict, dictionary with the owrds and the number of times it repeats
        """
        doc = fitz.open(self.path)
        words = self.get_text_word()

        # flat any structure
        flattener_words = []
        for item in words:
            if isinstance(item, list):
                # if is a list, extend with its elements
                flattener_words.extend([word for word in item if isinstance(word, str)])
            elif isinstance(item, str):
                #if is a string, add it directly
                flattener_words.append(str(item))
        
        # join and process
        all_text = ' '.join(flattener_words).lower()
        text = re.findall(r'\w+', all_text)
        v = Counter(text)
        v_sorted = dict(sorted(v.items(), key=lambda item: item[1], reverse=True))
        return v_sorted