""" Script where we use GPT-2 to generate text and save it in a pdf file """
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import textwrap

def generateTXT():
    ss 

def generateTXTconcat():
    ssss

def savePDF(text, filename="output.pdf"):
    """
    Saves a large text in a pdf file
    """
    c = canvas.Canvas(filename=filename, pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin
    
    # adjust the text in lines
    wrapped_text = textwrap.wrap(text=text, width=90)

    for line in wrapped_text:
        if y <= margin:
            c.showPage()
            y = height - margin
        c.drawString(margin, y, line)
        y -= 15 # space between lines
    
    c.save()
    print(f"Text saved in {filename}")

if __name__ == "__main__":
    # generate the text
    text = generateTXTconcat(
        model, tokenizer,
        prompt="Había una vez ",
        num_words=1000,
        block_size=150
    )

    # save the text in a pdf file
    savePDF(text=text, "example.pdf")