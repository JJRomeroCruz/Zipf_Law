import pandas as pd
import numpy as np
import fitz
import os
import re
from collections import Counter
import plotly.express as px

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
    # flat any structure
    flattened_words = []
    for item in words: 
        if isinstance(item, list):
            # if is a list, extend with its elements
            flattened_words.extend([word for word in item if isinstance(word, str)])
        elif isinstance(item, str):
            # if is a srting, add it directly
            flattened_words.append(str(item))
    
    # join and process
    all_text = ' '.join(flattened_words).lower()
    text = re.findall(r'\w+', all_text)
    v = Counter(text)
    v_sorted = dict(sorted(v.items(), key=lambda item: item[1], reverse=True))
    return v_sorted

import plotly.express as px
import pandas as pd

def interactive_word_plot(word_count_dict, top_n=50):
    """
    Scatter plot interactivo con Plotly
    """
    sorted_words = sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)
    top_words = sorted_words[:top_n]
    
    # Crear DataFrame
    df = pd.DataFrame(top_words, columns=['Palabra', 'Frecuencia'])
    df['Rango'] = range(1, len(df) + 1)
    
    fig = px.scatter(df, x='Rango', y='Frecuencia', 
                    size='Frecuencia', hover_name='Palabra',
                    title=f'Frecuencia de las {top_n} palabras más comunes',
                    size_max=60, color='Frecuencia',
                    labels={'Frecuencia': 'Frecuencia', 'Rango': 'Rango'})
    
    fig.update_traces(marker=dict(opacity=0.7),
                     hovertemplate='<b>%{hovertext}</b><br>Rango: %{x}<br>Frecuencia: %{y}')
    
    fig.show()

#interactive_word_plot(v, top_n=50)


