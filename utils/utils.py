import pandas as pd
import numpy as np
import fitz
import os
import re
from collections import Counter
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

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



def interactive_word_plot(word_count_dict, top_n=50):
    """
    Scatter plot interactivo con Plotly
    """
    sorted_words = sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)
    top_words = sorted_words[:top_n]
    
    # create the dataframe 
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


def plot_frequency_scatter(word_dict, top_n=50):
    """
    
    """
    # sort by frequency and take the top n
    sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
    top_words = sorted_words[:top_n]

    words = [item[0] for item in top_words]
    frequencies = [item[1] for item in top_words]
    positions = range(len(words))

    plt.figure(figsize=(15, 8))
    plt.scatter(positions, frequencies, alpha=0.6, color='steelblue')

    # añadimos etiquetas de palabras
    for i, word in enumerate(words):
        plt.annotate(word, (i, frequencies[i]),
                     xytext=(5, 5), textcoords='offset points',
                     fontsize=9, alpha=0.8, rotation=45)
    
    plt.xlabel('Palabras')
    plt.ylabel('Frecuencia')

    plt.title(f'Frencuencia de las {top_n} palabras mas comunes')
    plt.grid(True, alpha=0.3)
    plt.xticks([]) # se ocultan los numeros del eje x
    plt.tight_layout()
    plt.show()

def plot_word_freq_log(word_dict, top_n=50):
        
        """
        
        """
        sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
        top_words = sorted_words[:top_n]

        words = [item[0] for item in top_words]
        frequencies = [item[1] for item in top_words]
        ranks = range(1, len(words) + 1)

        plt.figure(figsize=(12, 8))
        plt.scatter(ranks, frequencies, alpha=0.6, s=50, color='red')
        plt.xscale('log')
        plt.yscale('log')

        # etiquetas algunas palabras clave
        for i in [0, len(words)//4, len(words)//2, -1]: # primera, 1/4, mitad, ultima
            plt.annotate(words[i], (ranks[i], frequencies[i]), 
                        xytext=(5, 5), textcoords='offset points', 
                        fontsize=9, alpha=0.8)
            
        plt.xlabel('Rango (log scale)')
        plt.ylabel('Frecuencia (log scale)')
        plt.title('Ley de Zipf: Frecuencia vs Rango (escala logaritmica)')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

def complete_analysis(word_dict, top_n=50):
    """
    Complete analysis with several visualizations
    """
    sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
    top_words = sorted_words[:top_n]

    words = [item[0] for item in top_words]
    frequencies = [item[1] for item in top_words]
    ranks = range(1, len(words) + 1)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

    # First graph, linear scatter
    ax1.scatter(range(len(words)), frequencies, s=100, alpha=0.7, color='steelblue')
    ax1.set_xlabel('Palabras')
    ax1.set_ylabel('Frecuencia')
    ax1.set_title(f'Top {top_n} most frequent words')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks([])

    # Second graph, log scatter
    ax2.scatter(ranks, frequencies, s=80, alpha=0.7, color='coral')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Rank (log scale)')
    ax2.set_ylabel('Frequency (log scale)')
    ax2.set_title("Zipf Law: Frequency vs Rank")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # statistics
    total_words = sum(word_dict.values())
    unique_words = len(word_dict)
    print(f'Number of words: {total_words}')
    print(f"Unique words: {unique_words}")
    print(f"Most frequent word: {words[0]} ({frequencies[0]} times)")

def combine(book1, book2):
    """
    Args: 

    Returns: 
    """
    # load the two books

    # tokenize the text

    # combine the two texts

