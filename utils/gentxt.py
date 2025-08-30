""" Script where we use GPT-2 to generate text and save it in a pdf file """
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import textwrap

def generateTXTconcat(model, tokenizer, prompt, num_words=2000, block_size=200, temperature=0.9):
    """
    Args: 
        model: language model
        tokenizer: tokenizer associated to the model
        prompt (str): Initial text
        num_words (int): Aproximate number of words to generate
        block_size (int): words for each block
        temperature (float): Randomness controller
    Returns: 
        str: text generated
    """
    local_path = "models"

    tokenizer = GPT2Tokenizer.from_pretrained(local_path, local_files_only=True)
    model = GPT2LMHeadModel.from_pretrained(local_path, local_files_only=True)

    tokenizer.pad_token = tokenizer.eos_token
    
    generated_text = prompt
    current_words = len(generated_text)

    # use the gpu if avaliable
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #model = model.to(device)
    max_context = 300

    while current_words < num_words:
        #input_ids = tokenizer.encode(generated_text, return_tensors="pt", truncation=True).to(device)
        input_ids = tokenizer("Había una vez un niño llamado ", 
                              return_tensors="pt", 
                              padding=True, 
                              truncation=True,
                              max_length=max_context
                              )

        output_ids = model.generate(
            input_ids["input_ids"],
            max_length=input_ids["input_ids"].shape[1] + block_size * 2,  # más tokens que palabras
            attention_mask=input_ids["attention_mask"],
            do_sample=True,
            top_k=50,
            top_p=0.9,
            temperature=temperature,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id
        )

        new_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # add the other generated in the last block
        generated_text = new_text
        current_words = len(generated_text.split())

        print(f"Progress: {current_words}/{num_words} words")

    return generated_text

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
    local_path = "models"
    tokenizer = GPT2Tokenizer.from_pretrained(local_path, local_files_only=True)
    model = GPT2LMHeadModel.from_pretrained(local_path, local_files_only=True)
    text = generateTXTconcat(
        model, tokenizer,
        prompt="Había una vez ",
        num_words=1000,
        block_size=150
    )

    # save the text in a pdf file
    savePDF(text=text, filename="example.pdf")