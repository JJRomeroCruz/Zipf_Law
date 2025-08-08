import pandas as pd
import numpy as np
import fitz
import os
import re
from collections import Counter

def PDFtoTXT(path):
    """
    Args:
        path: string, the path to the pdf file

    Returns: 
    """
    doc = fitz.open(path)
    output = open("output.txt", 'wb')
    for page in doc:
        text = page.get_text().encode('utf8')
        output.write(text)
        output.write(bytes((12,)))
    output.close()
    return

def PDFtoNumpy(path):
    """
    Args:
        path: string, the path to the pdf file

    Returns:
        text
    """
    doc = fitz.open(path)
    output = []
    for page in doc:
        text = page.get_text()
        output.append(text)
    return np.array(output)

def pdf2words(pdf_file):
    """
    Args: 

    Return:
    """
    words = []

    # open the pdf file
    pdf_document = fitz.open(pdf_file)

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        text = page.get_text()

        # divide the text in words if there is an spacce between them
        word_list = re.findall(r'\b\w+\b', text)

        words.extend(word_list)
    
    return words

def count_words(words):
    """
    Args:  
        words: list, the array of words we want to count

    Returns: 
        v_sorted: dict, dictionary with the owrds and the number of times it repeats
    """
    v = Counter(words)
    v_sorted = dict(sorted(v.items(), key=lambda item: item[1]))
    return v_sorted


