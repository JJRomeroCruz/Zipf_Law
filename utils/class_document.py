import fitz
import re
import pandas as pd
import nltk

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