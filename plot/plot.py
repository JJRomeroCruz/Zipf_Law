import pandas as pd
import numpy as np
import fitz
import os
import re
from collections import Counter
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

def interactive_word_plot(word_count_dict, top_n=50):
    """
    Scatter plot interactivo con Plotly
    """
    sorted_words = sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)
    top_words = sorted_words[:top_n]
    
    # create the dataframe 
    df = pd.DataFrame(top_words, columns=['Palabra', 'Frecuencia'])
    #df['Rango'] = range(1, len(df) + 1)
    df['Rango'] = [len(item) for item in df["Palabra"]]
    
    """
    fig = px.scatter(df, x='Rango', y='Frecuencia', 
                    size='Frecuencia', hover_name='Palabra',
                    title=f'Frecuencia de las {top_n} palabras más comunes',
                    size_max=60, color='Frecuencia',
                    labels={'Frecuencia': 'Frecuencia', 'Rango': 'Rango'})
    """
    fig = px.scatter(df, y='Frecuencia', 
                    size='Frecuencia', hover_name='Palabra',
                    title=f'Frecuencia de las {top_n} palabras más comunes',
                    size_max=60, color='Frecuencia',
                    labels={'Frecuencia': 'Frecuencia', 'Rango': 'Rango'})
    
    fig.update_traces(marker=dict(opacity=0.7),
                     hovertemplate='<b>%{hovertext}</b><br>Rango: %{df["Rango"]}<br>Frecuencia: %{y}')
    
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